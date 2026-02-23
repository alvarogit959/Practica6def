from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RepartoWizard(models.TransientModel):
    _name = 'reparto.reparto_wizard'

    empleado_id = fields.Many2one('reparto.empleado', string="Empleado", required=True)
    vehiculo_id = fields.Many2one('reparto.vehiculo', string="Vehículo", required=True)
    cliente_id = fields.Many2one('reparto.cliente', string="Cliente", required=True)

    def crear_reparto(self):
        Reparto = self.env['reparto.reparto']

#Crear el reparto
        reparto = Reparto.new({
            'empleado_id': self.empleado_id.id,
            'vehiculo_id': self.vehiculo_id.id,
            'cliente_id': self.cliente_id.id,
            'fecha_recepcion': fields.Datetime.now(),
            'estado': 'camino',
        })

        reparto._check_carnet()
        reparto._check_reparto_activo()
        reparto._check_km()
        reparto_id = Reparto.create(reparto._convert_to_write(reparto._cache))
        return {'type': 'ir.actions.act_window_close'}
