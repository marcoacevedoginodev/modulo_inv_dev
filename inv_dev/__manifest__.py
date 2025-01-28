{
    'name': 'Generacion de Etiquetas ZPL',
    'version': '1.0',
    'summary': 'Modulo para generar etiquetas ZPL',
    'description': 'Permite generar etiquetas ZPL para productos.',
    'author': 'Tu Nombre',
    'depends': ['product', 'stock'],
    'data': [
        'security/ir.model.access.csv',  
        'views/inv_model_views.xml',    
    ],
    'installable': True,
    'application': True,
}