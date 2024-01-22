#-*- coding:utf-8 -*-
from odoo import api, models

class PayslipDetailsReportWorkedDays(models.AbstractModel):
    _name = 'report.hr_payroll_worked_days_report.report_payslip_worked_days'
    _description = 'Payslip Worked Days Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        payslips = self.env['hr.payslip'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': payslips,
            'data': data,
            'test1': 'Test1',
        }
