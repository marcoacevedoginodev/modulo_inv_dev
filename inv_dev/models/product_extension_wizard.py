from odoo import models, fields, api
import os
import logging

_logger = logging.getLogger(__name__)

class ProductExtensionWizard(models.TransientModel):
    _name = 'product.extension.wizard'
    _description = 'Product Extension Wizard'

    id_codigo = fields.Integer(string='Codigo')
    id_numero = fields.Integer(string='Numero')
    cantidad = fields.Integer(string='Cantidad')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('id_codigo_unique', 'UNIQUE(id_codigo, active)', 'El codigo debe ser único.')
    ]

    @api.model
    def generate_zpl_label(self, *args, **kwargs):
        zpl_labels = []
        for record in self:
            zpl = f"""
            ^XA
            ^FO50,50 
            ^B3N,N,100,Y,N
            ^FD>: {record.id_codigo}^FS
            ^FO50,200
            ^A0N,50,50
            ^FDNumero: {record.id_numero}^FS
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
        file_path = r'C:\Users\macevedo\Desktop\modulo_inv_dev\etiqueta_zpl.txt'
        try:
            with open(file_path, 'w') as file:
                file.write(zpl + '\n')
            return file_path
        except Exception as e:
            _logger.error(f"Error writing ZPL file: {e}")
            return False

    @api.model
    def create_and_generate_zpl(self, vals):
        file_path = self.create_zpl_file()
        return file_path

    def unlink(self):
        return True
