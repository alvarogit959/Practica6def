from odoo import models, fields, api

class Vehiculo(models.Model):
    _name = 'reparto.vehiculo'

    tipo = fields.Selection([
        ('bicicleta', 'Bicicleta'),
        ('furgoneta', 'Furgoneta')
    ], required=True)

    matricula = fields.Char()
    foto = fields.Binary()
    descripcion = fields.Text()

    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('reparto', 'En reparto')
    ], default='disponible')
