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
    cantidad = fields.Float(string="Cantidad", default=0.0, required=True)
    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string="Nombre")

    _sql_constraints = [
        ('id_codigo_unique', 'UNIQUE(id_codigo, active)', 'El codigo debe ser único.')
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = 'Producto sin nombre'
        return super(ProductExtensionWizard, self).create(vals)

    def write(self, vals):
        if 'name' not in vals and not self.name:
            vals['name'] = 'Producto sin nombre'
        return super(ProductExtensionWizard, self).write(vals)
        
    @api.model
    def generate_zpl_label(self, *args, **kwargs):
        zpl_labels = []
        for record in self:
            zpl = f"""
            ^XA
            ^FO50,50 
            ^B3N,N,100,Y,N
            ^FD>: {record.id_codigo.name}^FS 
            ^FO50,200
            ^A0N,50,50
            ^FDNumero: {record.id_numero.name}^FS  
            ^FO50,300
            ^A0N,50,50
            ^FDCantidad: {record.cantidad}^FS
            ^FO50,400
            ^GB800,3,3^FS            
            ^XZ
            """

            zpl_labels.append(zpl)
        return zpl_labels
        
    def create_zpl_file(self):
        zpl = self.generate_zpl_label()
        if not zpl:
            _logger.error("No se generaron etiquetas ZPL.")
            return False
        file_path = r'C:/home/lortiz/etiqueta_zpl.txt'
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            with open(file_path, 'w') as file:
                file.write(zpl[0] + '\n') 
            return file_path
        except Exception as e:
            _logger.error(f"Error escribiendo el archivo ZPL: {e}")
            return False
    
    @api.model
    def create_and_generate_zpl(self, vals):
        record = self.create(vals)
        file_path = record.create_zpl_file()
        return file_path

    def unlink(self):
        for record in self:
            record.active = False
        return super(ProductExtensionWizard, self).unlink()
