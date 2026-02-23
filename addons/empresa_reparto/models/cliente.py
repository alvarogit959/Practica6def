from odoo import models, fields, api

class Cliente(models.Model):
    _name = 'reparto.cliente'

    dni = fields.Char(required=True)
    nombre = fields.Char(required=True)
    apellidos = fields.Char()
    telefono = fields.Char()
