# -*- coding: utf-8 -*-
{
    'name': "Dental Clinic",

    'summary': "System management for dental clinics.",

    'description': """
    Dental Clinic by full automation system
    """,

    'author': "Eng. Seif Hany",
    'website': "https://www.linkedin.com/in/seif-el-baghdady-8244b229a/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Health Care/Clinic',
    'version': '17.0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'web','inventory'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        ############################################
        'views/booking/booking.xml',
        'views/booking/booking_line.xml',
        ############################################
        'views/system/teeth/tooth.xml',
        'views/system/teeth/teeth.xml',
        'views/system/cost_examination.xml',
        'views/system/general_diagnosis.xml',
        'views/system/job.xml',
        'views/system/medical_history.xml',
        ############################################
        'report/patient_report.xml',
        'report/template.xml',
        ############################################
        # 'report/patient_report_2.xml',
        # 'report/template_2.xml',
        ############################################
        'report/patient_report_3.xml',
        'report/template_3.xml',
        ############################################

        'views/dashboardViews.xml',

        'views/views.xml',

        'views/menu.xml',

    ],

    'qweb': [
        'dental_clinic/static/src/dashboard/dashboard.xml',

    ],

    'assets': {
        'web.assets_backend': [
            'dental_clinic/static/src/dashboard/dashboard.js',
            'dental_clinic/static/src/dashboard/dashboard.css',

        ],
    },


    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'auto_install': False,

}



