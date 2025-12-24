{
    'name': "Inventory Clinic",

    'summary': "Inventory and suppliers management system for dental clinics (materials, medicines, tools, devices, stock, and purchase orders).",

    'description': """
        The Inventory Clinic module provides a specialized system to manage dental clinic supplies and stock:
    """,

    'author': "Eng. Seif Hany",
    'website': "https://www.linkedin.com/in/seif-el-baghdady-8244b229a/",

    'category': 'Health Care/Clinic',
    'version': '17.0.1.0',

    'depends': ['base','mail'],


    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/product.xml',
        'views/vendor.xml',
        'views/menu.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
