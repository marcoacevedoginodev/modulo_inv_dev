from odoo import models, fields, api

class Codigo(models.Model):
    _name = 'product.codigo'
    _description = 'Codigo'

    name = fields.Char(string="Codigo")

class Numero(models.Model):
    _name = 'product.numero'
    _description = 'Numero'

    name = fields.Char(string="Numero")

class Cantidad(models.Model):    
    _name = 'product.cantidad'
    _description = 'Cantidad'

    name = fields.Float(string="Cantidad", default=0.0)

class ProductExtension(models.Model):
    _inherit = 'product.product'

    id_codigo = fields.Many2one('product.codigo', string="Codigo", required=True)
    id_numero = fields.Many2one('product.numero', string="Numero", required=True)
    cantidad = fields.Float(string="Cantidad", default=0.0, required=True)

    name = fields.Char(string="Nombre")

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = 'Producto sin nombre'
        return super(ProductExtension, self).create(vals)

    def write(self, vals):
        if 'name' not in vals and not self.name:
            vals['name'] = 'Producto sin nombre'
        return super(ProductExtension, self).write(vals)


