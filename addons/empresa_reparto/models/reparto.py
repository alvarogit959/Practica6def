from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Reparto(models.Model):
    _name = 'reparto.reparto'
    _description = 'Reparto'
    _order = 'fecha_recepcion desc, urgencia'

    codigo = fields.Char(default='Nuevo', readonly=True)
    fecha_inicio = fields.Datetime()
    fecha_retorno = fields.Datetime()
    fecha_recepcion = fields.Datetime(required=True)

    empleado_id = fields.Many2one('reparto.empleado', required=True)
    vehiculo_id = fields.Many2one('reparto.vehiculo', required=True)
    kilometros = fields.Float()
    peso = fields.Float()
    volumen = fields.Float()
    observaciones = fields.Text()

    estado = fields.Selection([
        ('no_salido', 'No ha salido'),
        ('camino', 'En camino'),
        ('entregado', 'Entregado')
    ], default='no_salido')

    urgencia = fields.Selection([
        ('organos', 'Órganos humanos'),
        ('refrigerado', 'Alimentos refrigerados'),
        ('alimentos', 'Alimentos'),
        ('alta', 'Alta prioridad'),
        ('baja', 'Baja prioridad')
    ])

    cliente_id = fields.Many2one('reparto.cliente')
    receptor = fields.Char()
#GENERADOR DE CODIGO  
    @api.model
    def create(self, vals):

        if vals.get('codigo', 'Nuevo') == 'Nuevo':
            vals['codigo'] = self.env['ir.sequence'].next_by_code('reparto.reparto') or 'Nuevo'
        return super(Reparto, self).create(vals)

    @api.constrains('empleado_id', 'vehiculo_id')
    def _check_carnet(self):
        for record in self:
            if record.vehiculo_id.tipo == 'bicicleta' and not record.empleado_id.carnet_ciclomotor:
                raise ValidationError("El empleado no tiene carnet de ciclomotor.")
            if record.vehiculo_id.tipo == 'furgoneta' and not record.empleado_id.carnet_furgoneta:
                raise ValidationError("El empleado no tiene carnet de furgoneta.")

    @api.constrains('empleado_id', 'estado')
    def _check_reparto_activo(self):
        for record in self:
            activos = self.search([
                ('empleado_id', '=', record.empleado_id.id),
                ('estado', '=', 'camino'),
                ('id', '!=', record.id)
            ])
            if activos and record.estado == 'camino':
                raise ValidationError("El empleado ya tiene un reparto activo.")
                
    @api.constrains('vehiculo_id', 'estado')
    def _check_vehiculo_activo(self):
        for record in self:
            if record.estado == 'camino':
                activos = self.search([
                    ('vehiculo_id', '=', record.vehiculo_id.id),
                    ('estado', '=', 'camino'),
                    ('id', '!=', record.id)
                ])
                if activos:
                    raise ValidationError("El vehículo ya está en otro reparto activo.")
                    
    @api.constrains('kilometros', 'vehiculo_id')
    def _check_km(self):
        for record in self:
            if record.vehiculo_id.tipo == 'bicicleta' and record.kilometros > 10:
                raise ValidationError("Más de 10km no puede hacerse en bicicleta.")
            if record.vehiculo_id.tipo == 'furgoneta' and record.kilometros < 1:
                raise ValidationError("Menos de 1km no puede hacerse en furgoneta.")

