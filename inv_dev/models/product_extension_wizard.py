from odoo import models, fields, api

class ProductExtensionWizard(models.TransientModel):
    _name = 'product.extension.wizard'
    _description = 'Product Extension Wizard'

    id_codigo = fields.Integer(string='Codigo')
    id_numero = fields.Integer(string='Numero')
    cantidad = fields.Integer(string='Cantidad')

    @api.model
    def generate_zpl_label(self):
        pass
