from odoo import models, fields, api

class ProductExtensionWizard(models.TransientModel):
    _name = 'product.extension.wizard'
    _description = 'Product Extension Wizard'

    id_codigo = fields.Integer(string='Codigo')
    id_numero = fields.Integer(string='Numero')
    cantidad = fields.Integer(string='Cantidad')

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
