# -*- coding: utf-8 -*-
{
    'name': "Hr Payroll worked days report",

    'summary': """
            details report for worked days in payslip
        """,

    'description': """
        - payslip details report  for worked days attendance,leaves and global leaves
    """,

    'author': "Amr Gaber",
    'images': ['images/emp_background.jpg'],
    'website': "https://www.linkedin.com/in/amr-gaber-109b1616a/",
    'category': 'Employees',
    'version': '12.0.1',
    'depends': ['hr_payroll'],
    'license': 'AGPL-3',
    # always loaded
    'data': [
        'report/report_payslip_worked_days.xml',
        'report/hr_payslip.xml',
    ],
}