# -*- coding: utf-8 -*-
{
    'name': "GraphQL Odoo",

    'summary': """
        Este modulo crea una interfaz de programación de aplicaciones (API)""",

    'description': """
        El modulo crea una interfaz para que aplicaciones externas puedan interactuar con los datos
        de Odoo
    """,

    'author': "Alejandro Pérez Álvarez",
    'website': "http://www.ieslamarisma.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'API',
    'version': '0.1',
    "license": "LGPL-3",
    "development_status": "Beta",

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'graphql_base', 'agro_fres'],

    'data': [
        'views/parcel_views.xml',
        'views/product_template_view.xml',
        'security/ir.model.access.csv',
    ],
}
