# -*- coding: utf-8 -*-
{
    'name': 'Empresa de Repartos',
    'version': '1.0',
    'description': 'Gestión de repartos',
    'author': 'Tu Nombre',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/empleado_views.xml',
        'views/vehiculo_views.xml',
        'views/cliente_views.xml',
        'views/reparto_views.xml',
        'views/menu.xml',
        'reports/reparto_report.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}