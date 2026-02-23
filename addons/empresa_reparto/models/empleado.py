from odoo import models, fields, api

class Empleado(models.Model):
    _name = 'reparto.empleado'
    _description = 'Empleado'

    nombre = fields.Char(required=True)
    apellidos = fields.Char(required=True)
    dni = fields.Char(required=True)
    telefono = fields.Char()
    foto = fields.Binary()
    carnet_ciclomotor = fields.Boolean()
    carnet_furgoneta = fields.Boolean()

    reparto_ids = fields.One2many('reparto.reparto', 'empleado_id')

    def open_repartos_pendientes(self):
        """Abre el informe de repartos"""
        self.ensure_one()

        action = self.env.ref('empresa_reparto.action_report_reparto', raise_if_not_found=False)
        if not action:

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'No se encontró la acción del informe',
                    'type': 'danger',
                    'sticky': True,
                }
            }
        return action.report_action(self)