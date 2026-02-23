from odoo import http
from odoo.http import request
import json

class RepartoController(http.Controller):

    @http.route('/repartos/estado/<string:codigo_reparto>', type='http', auth='public', methods=['GET'], csrf=False)
    def obtener_estado_reparto(self, codigo_reparto, **kwargs):
        try:
            reparto = request.env['reparto.reparto'].sudo().search([
                ('codigo', '=', codigo_reparto)
            ], limit=1)
#test error de id
            if not reparto and codigo_reparto.isdigit():
                reparto = request.env['reparto.reparto'].sudo().browse(int(codigo_reparto))
            
            if not reparto:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'error': f'No se encontró el reparto con código: {codigo_reparto}'
                    }, ensure_ascii=False),
                    headers=[('Content-Type', 'application/json')]
                )
            
#Obtener la info 
            estado_texto = dict(reparto._fields['estado'].selection).get(reparto.estado)
            urgencia_texto = dict(reparto._fields['urgencia'].selection).get(reparto.urgencia)
            
            resultado = {
                'success': True,
                'data': {
                    'codigo': reparto.codigo,
                    'id': reparto.id,
                    'estado': reparto.estado,
                    'estado_descripcion': estado_texto,
                    'urgencia': reparto.urgencia,
                    'urgencia_descripcion': urgencia_texto,
                    'fecha_recepcion': reparto.fecha_recepcion.strftime('%d/%m/%Y %H:%M') if reparto.fecha_recepcion else None,
                    'fecha_inicio': reparto.fecha_inicio.strftime('%d/%m/%Y %H:%M') if reparto.fecha_inicio else None,
                    'fecha_retorno': reparto.fecha_retorno.strftime('%d/%m/%Y %H:%M') if reparto.fecha_retorno else None,
                    'repartidor': {
                        'id': reparto.empleado_id.id,
                        'nombre': reparto.empleado_id.nombre,
                        'apellidos': reparto.empleado_id.apellidos,
                        'dni': reparto.empleado_id.dni
                    } if reparto.empleado_id else None,
                    'vehiculo': {
                        'id': reparto.vehiculo_id.id,
                        'tipo': reparto.vehiculo_id.tipo,
                        'descripcion': reparto.vehiculo_id.descripcion,
                        'matricula': reparto.vehiculo_id.matricula
                    } if reparto.vehiculo_id else None,
                    'cliente_emisor': {
                        'id': reparto.cliente_id.id,
                        'nombre': reparto.cliente_id.nombre,
                        'apellidos': reparto.cliente_id.apellidos,
                        'dni': reparto.cliente_id.dni
                    } if reparto.cliente_id else None,
                    'receptor': reparto.receptor,
                    'kilometros': reparto.kilometros,
                    'peso': reparto.peso,
                    'volumen': reparto.volumen,
                    'observaciones': reparto.observaciones
                }
            }
            
            return request.make_response(
                json.dumps(resultado, ensure_ascii=False),
                headers=[('Content-Type', 'application/json')]
            )
            
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'error': str(e)
                }, ensure_ascii=False),
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/repartos/estado', type='http', auth='public', methods=['GET'], csrf=False)
    def listar_repartos(self, **kwargs):
        try:
            repartos = request.env['reparto.reparto'].sudo().search([], limit=100)
            
            resultado = {
                'success': True,
                'total': len(repartos),
                'data': []
            }
            
            for reparto in repartos:
                estado_texto = dict(reparto._fields['estado'].selection).get(reparto.estado)
                resultado['data'].append({
                    'codigo': reparto.codigo,
                    'id': reparto.id,
                    'estado': reparto.estado,
                    'estado_descripcion': estado_texto,
                    'fecha_recepcion': reparto.fecha_recepcion.strftime('%d/%m/%Y %H:%M') if reparto.fecha_recepcion else None,
                    'repartidor': reparto.empleado_id.nombre if reparto.empleado_id else None,
                    'urgencia': reparto.urgencia
                })
            
            return request.make_response(
                json.dumps(resultado, ensure_ascii=False),
                headers=[('Content-Type', 'application/json')]
            )
            
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'error': str(e)
                }, ensure_ascii=False),
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/repartos/web/estado/<string:codigo_reparto>', type='http', auth='public', methods=['GET'], csrf=False)
    def web_estado_reparto(self, codigo_reparto, **kwargs):
        """
        Versión web con HTML para ver el estado de un reparto
        Ejemplo: http://localhost:8069/repartos/web/estado/REP0001
        """
        reparto = request.env['reparto.reparto'].sudo().search([
            ('codigo', '=', codigo_reparto)
        ], limit=1)
        
        if not reparto and codigo_reparto.isdigit():
            reparto = request.env['reparto.reparto'].sudo().browse(int(codigo_reparto))
        
        if not reparto:
            return """
            <html>
                <head><title>Reparto no encontrado</title></head>
                <body>
                    <h1>Error</h1>
                    <p>No se encontró el reparto con código: {}</p>
                </body>
            </html>
            """.format(codigo_reparto)
#test, no funciona 
        color_estado = {
            'no_salido': 'gray',
            'camino': 'orange',
            'entregado': 'green'
        }.get(reparto.estado, 'black')
        
        estado_texto = dict(reparto._fields['estado'].selection).get(reparto.estado)
        urgencia_texto = dict(reparto._fields['urgencia'].selection).get(reparto.urgencia)
        
        return """
        <html>
            <head>
                <title>Estado del Reparto {}</title>
                <style>
                    body {{ font-family: Arial; margin: 40px; }}
                    .card {{ border: 1px solid #ddd; padding: 20px; border-radius: 5px; }}
                    .estado {{ color: {}; font-weight: bold; }}
                    .label {{ font-weight: bold; color: #666; }}
                </style>
            </head>
            <body>
                <h1>Estado del Reparto {}</h1>
                <div class="card">
                    <p><span class="label">Código:</span> {}</p>
                    <p><span class="label">Estado:</span> <span class="estado">{}</span></p>
                    <p><span class="label">Urgencia:</span> {}</p>
                    <p><span class="label">Fecha recepción:</span> {}</p>
                    <p><span class="label">Repartidor:</span> {} {}</p>
                    <p><span class="label">Vehículo:</span> {} - {}</p>
                    <p><span class="label">Cliente emisor:</span> {} {}</p>
                    <p><span class="label">Receptor:</span> {}</p>
                    <p><span class="label">Kilómetros:</span> {} km</p>
                    <p><span class="label">Peso:</span> {} kg</p>
                    <p><span class="label">Volumen:</span> {}</p>
                </div>
            </body>
        </html>
        """.format(
            reparto.codigo,
            color_estado,
            reparto.codigo,
            reparto.codigo,
            estado_texto,
            urgencia_texto,
            reparto.fecha_recepcion.strftime('%d/%m/%Y %H:%M') if reparto.fecha_recepcion else 'N/A',
            reparto.empleado_id.nombre or '', reparto.empleado_id.apellidos or '',
            reparto.vehiculo_id.tipo or '', reparto.vehiculo_id.descripcion or '',
            reparto.cliente_id.nombre or '', reparto.cliente_id.apellidos or '',
            reparto.receptor or 'N/A',
            reparto.kilometros or 0,
            reparto.peso or 0,
            reparto.volumen or 0
        )