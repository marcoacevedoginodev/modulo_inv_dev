from odoo import models, fields, api
from odoo.exceptions import UserError
import base64

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

    id_codigo = fields.Many2one('product.codigo', string="Codigo")
    id_numero = fields.Many2one('product.numero', string="Numero")
    id_cantidad = fields.Many2one('product.cantidad', string="Cantidad")

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

    
class ProductExtensionWizard(models.TransientModel):
    _name = 'product.extension.wizard'
    _description = 'Product Extension Wizard'

    id_codigo = fields.Many2one('product.codigo', string="Codigo", required=True)
    id_numero = fields.Many2one('product.numero', string="Numero", required=True)
    id_cantidad = fields.Many2one('product.cantidad', string="Cantidad", required=True)

    def generate_zpl_label(self):
        self.ensure_one()
        zpl = f"""
        ^XA
        ^FO50,50 
        ^B3N,N,100,Y,N
        ^FD>: {self.id_codigo.name}^FS
        ^FO50,200
        ^A0N,50,50
        ^FDNumero: {self.id_numero.name}^FS
        ^FO50,300
        ^A0N,50,50
        ^FDCantidad: {self.id_cantidad.name}^FS
        ^FO50,400
        ^GB800,3,3^FS            
        ^FO50,550
        ^B3N,N,100,Y,N
        ^FD>: {self.id_codigo.name}^FS
        ^XZ
        """
        return zpl

    def preview_zpl_label(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/product/label/{self.id}/preview',
            'target': 'self',
        }
