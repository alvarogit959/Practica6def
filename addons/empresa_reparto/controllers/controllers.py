from odoo import http
from odoo.http import request

class RepartoController(http.Controller):

    @http.route('/estado_reparto/<string:codigo>', auth='public')
    def estado_reparto(self, codigo):
        reparto = request.env['reparto.reparto'].sudo().search([('codigo','=',codigo)], limit=1)
        if reparto:
            return f"Estado: {reparto.estado}"
        else:
            return "No encontrado"

