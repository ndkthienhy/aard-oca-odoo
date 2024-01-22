# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import babel
from datetime import date, datetime, time,timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone, UTC

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'Pay Slip'

    def date_range(self, date_from, date_to):
        lst_date_range = []
        delta = date_to - date_from
        for i in range(delta.days + 1):
            day = date_from + timedelta(days=i)
            lst_date_range.append(day)
        return lst_date_range

    def get_leave_name(self, leave):
        return leave.holiday_id.holiday_status_id.name

    @api.model
    def get_worked_day_lines_more_details(self, contracts, date_from, date_to):
        day_state_list = []
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            for day in self.date_range(fields.Date.from_string(date_from),
                                       fields.Date.from_string(date_to)):
                day_min = datetime.combine(day, time.min)
                day_max = datetime.combine(day, time.max)
                leaves = {}
                calendar = contract.resource_calendar_id
                tz = timezone(calendar.tz)
                user_tz = self.env.user.tz or 'UTC'
                # check day is working day or not:
                work_time_days = contract.employee_id.list_work_time_per_day(day_min, day_max,
                                                                             calendar=contract.resource_calendar_id)
                # check day is leave
                day_leave_intervals = contract.employee_id.list_leaves(day_min, day_max, calendar=contract.resource_calendar_id)

                if work_time_days:
                    for work_time in work_time_days:
                        domain_attend = [('employee_id', '=', contract.employee_id.id),
                                         ('check_in', '>=', work_time[0]),
                                         ('check_in', '<=', work_time[0])]
                        attendances = self.env["hr.attendance"].search(domain_attend)
                        if attendances:
                            for attend in attendances:
                                hours = '{0:02.0f}:{1:02.0f}'.format(*divmod(attend['worked_hours'] * 60, 60))
                                localize_dt = timezone('UTC').localize(attend.check_in).astimezone(timezone(user_tz))
                                from_time = localize_dt.time()
                                localize_dt = timezone('UTC').localize(attend.check_out).astimezone(timezone(user_tz))
                                to_time = localize_dt.time()
                                day_state = {
                                    'day': day,
                                    'day_name': day.strftime("%A"),
                                    'status': 'Attendance',
                                    'hours': hours,
                                    'from_time': from_time,
                                    'to_time': to_time,
                                }
                                day_state_list.append(day_state)
                        else:
                            day_state = {
                                'day': day,
                                'day_name': day.strftime("%A"),
                                'status': 'Absence',
                                'hours': None,
                                'from_time': None,
                                'to_time': None,
                            }
                            day_state_list.append(day_state)

                if day_leave_intervals:
                    for day, hours, leave in day_leave_intervals:
                        hours = '{0:02.0f}:{1:02.0f}'.format(*divmod(hours * 60, 60))
                        localize_dt = timezone('UTC').localize(leave.date_from).astimezone(timezone(user_tz))
                        from_time = localize_dt.time()
                        localize_dt = timezone('UTC').localize(leave.date_to).astimezone(timezone(user_tz))
                        to_time = localize_dt.time()
                        day_state = {
                            'day': day,
                            'day_name': day.strftime("%A"),
                            'status': self.get_leave_name(leave) or _('Global Leaves'),
                            'hours': hours,
                            'from_time': from_time,
                            'to_time': to_time,
                        }
                        day_state_list.append(day_state)
                # not attend,absence and leave so it will be weekend
                if not day_leave_intervals and not work_time_days:
                    day_state = {
                        'day': day,
                        'day_name': day.strftime("%A"),
                        'status': _('Weekend'),
                        'hours': None,
                        'from_time': None,
                        'to_time': None,
                    }
                    day_state_list.append(day_state)
        return day_state_list
