from odoo import models, fields, api
import os
import logging

_logger = logging.getLogger(__name__)

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

class ProductExtensionWizard(models.TransientModel):
    _name = 'product.extension.wizard'
    _description = 'Product Extension Wizard'

    id_codigo = fields.Many2one('product.codigo', string="Codigo", required=True)
    id_numero = fields.Many2one('product.numero', string="Numero", required=True)
    cantidad = fields.Integer(string="Cantidad", default=0.0, required=True)
    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string="Nombre")
    zpl_content = fields.Text(string="ZPL Content", readonly=True)

    _sql_constraints = [
        ('id_codigo_unique', 'UNIQUE(id_codigo, active)', 'el codigo debe ser único.')
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = 'producto sin nombre'
        return super(ProductExtensionWizard, self).create(vals)

    def write(self, vals):
        if 'name' not in vals and not self.name:
            vals['name'] = 'producto sin nombre'
        return super(ProductExtensionWizard, self).write(vals)
        
    @api.model
    def generate_zpl_label(self, vals):
        codigo_record = self.env['product.codigo'].browse(vals.get('id_codigo'))
        numero_record = self.env['product.numero'].browse(vals.get('id_numero'))
        codigo = codigo_record.name if codigo_record else 'Desconocido'
        numero = numero_record.name if numero_record else 'Desconocido'
        cantidad = vals.get('cantidad', 0)

        zpl = f"""
        ^XA
        ^FO50,50 
        ^B3N,N,100,Y,N
        ^FD>: {codigo}^FS 
        ^FO50,200
        ^A0N,50,50
        ^FDNumero: {numero}^FS  
        ^FO50,300
        ^A0N,50,50
        ^FDCantidad: {cantidad}^FS
        ^FO50,400
        ^GB800,3,3^FS            
        ^XZ
        """
        return zpl.strip()

    def create_and_generate_zpl(self):
        vals = {
            'id_codigo': self.id_codigo.id if self.id_codigo else '',
            'id_numero': self.id_numero.id if self.id_numero else '',
            'cantidad': self.cantidad
        }
        zpl = self.generate_zpl_label(vals)

        file_path = '/tmp/etiqueta_zpl.txt'
        directory = os.path.dirname(file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            with open(file_path, 'w') as file:
                file.write(zpl + '\n')
            _logger.info(f"etiqueta guardada en {file_path}")
        except Exception as e:
            _logger.error(f"error: {e}")
            return {'warning': {'title': "Error", 'message': "no se pudo guardar el archivo."}}

        return {
            'warning': {
                'title': "Éxito",
                'message': f"etiqueta ZPL generada y guardada en {file_path}."
            }
        }

    def unlink(self):
        for record in self:
            record.active = False
        return super(ProductExtensionWizard, self).unlink()
