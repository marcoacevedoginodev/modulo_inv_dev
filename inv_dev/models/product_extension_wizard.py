from odoo import models, fields, api  
import os  
import logging  
# se configura el logger
_logger = logging.getLogger(__name__)  
# define el modelo
class Codigo(models.Model):
    # nombre de modelo en odoo  
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
        # restriccion sql para que no se repìta el codigo
        ('id_codigo_unique', 'UNIQUE(id_codigo, active)', 'el codigo debe ser único.')  
    ]

    @api.model
    # metodo para crear un nuevo registro
    def create(self, vals):
        # si no ingreso nombre  
        if not vals.get('name'):
            # se asigna un nombre por defecto  
            vals['name'] = 'producto sin nombre'
        # llama al método 'create'              
        return super(ProductExtensionWizard, self).create(vals)  
    # metodo para actualizar un registro
    def write(self, vals):  
        if 'name' not in vals and not self.name: 
            vals['name'] = 'producto sin nombre' 
        return super(ProductExtensionWizard, self).write(vals)  
        
    @api.model
    # metodo para generar una etiqueta zpl
    def generate_zpl_label(self, vals):
        # obtiene 'product.codigo'  
        codigo_record = self.env['product.codigo'].browse(vals.get('id_codigo'))
        # obtiene 'product.numero'  
        numero_record = self.env['product.numero'].browse(vals.get('id_numero'))
        # asigna el nombre del codigo  
        codigo = codigo_record.name if codigo_record else 'Desconocido'
        # asigna el nombre del numero  
        numero = numero_record.name if numero_record else 'Desconocido'
        # obtiene la cantidad  
        cantidad = vals.get('cantidad', 0)  
        # define el contenido de la etiqueta
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
        # retorna el contenido zpl sin espacios en blanco 
        return zpl.strip()  
    # metodo para crear y generar etiqueta 
    def create_and_generate_zpl(self):  
        vals = {
            # obtiene el ID del codigo
            'id_codigo': self.id_codigo.id if self.id_codigo else '',
            # obtiene el ID del numero  
            'id_numero': self.id_numero.id if self.id_numero else '',
            # obtiene la cantidad  
            'cantidad': self.cantidad  
        }
        # genero la etiqueta
        zpl = self.generate_zpl_label(vals)  
        # ruta del archivo creado
        file_path = '/tmp/etiqueta_zpl.txt'
        # obtiene el directorio del archivo creado anteriormente  
        directory = os.path.dirname(file_path)  
        # si el directorio no existe en la ruta /tmp/ 
        if not os.path.exists(directory):
            # creo el directorio  
            os.makedirs(directory)  

        try:
            # abro el archivo con parametro w para escribir
            with open(file_path, 'w') as file:
                # escribo el contenido del formato zpl  
                file.write(zpl + '\n')  
            # mensaje ok para saber si realmente de creo el archivo    
            _logger.info(f"etiqueta guardada en {file_path}")  
        except Exception as e:  
            _logger.error(f"error: {e}")  
            # retorno mensaje de error
            return {'warning': {'title': "Error", 'message': "no se pudo guardar el archivo."}}  

        return {
            'warning': {
                'title': "Éxito",
                # retorna mensaje de creacion exitosa
                'message': f"etiqueta zpl generada y guardada en {file_path}."  
            }
        }
    # metodo para eliminar el registro
    def unlink(self):  
        # itero sobre los registros
        for record in self:  
            # marco el registro como inactivo por un error que me enviaba odoo
            record.active = False   
        return super(ProductExtensionWizard, self).unlink() 
