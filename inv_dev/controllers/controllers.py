from odoo import http
from odoo.http import request
import logging

class ProductExtensionController(http.Controller):
    _logger = logging.getLogger(__name__)

    @http.route('/product/label/<model("product.extension.wizard"):wizard_id>/download', type='http', auth='user')
    def download_zpl_label(self, wizard_id, **kw):
        try:
            self._logger.info("Generating ZPL label for wizard %s", wizard_id.id)
            zpl_content = wizard_id.generate_zpl_label()
            
            return request.make_response(
                zpl_content,
                headers=[('Content-Type', 'text/plain'),
                        ('Content-Disposition', f'attachment; filename=etiqueta_{wizard_id.id}.txt')]
            )
        except Exception as e:
            self._logger.error("Error generating ZPL label: %s", str(e))
            return request.make_response(
                f"Error generating ZPL label: {str(e)}",
                headers=[('Content-Type', 'text/plain')]
            )

    @http.route('/product/label/<model("product.extension.wizard"):wizard_id>/preview', type='http', auth='user')
    def preview_zpl_label(self, wizard_id, **kw):
        try:
            self._logger.info("Previewing ZPL label for wizard %s", wizard_id.id)
            zpl_content = wizard_id.generate_zpl_label()
            
            return request.make_response(
                zpl_content,
                headers=[('Content-Type', 'text/plain')]
            )
        except Exception as e:
            self._logger.error("Error previewing ZPL label: %s", str(e))
            return request.make_response(
                f"Error previewing ZPL label: {str(e)}",
                headers=[('Content-Type', 'text/plain')]
            )

    @http.route('/404', type='http', auth='public', website=True)
    def custom_404(self, **kw):
        return request.render('your_module.404_template', {})