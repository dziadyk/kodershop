
from odoo import _, fields, models


class Car(models.Model):
    _name = 'parking.center.car'
    _description = 'Car'

    name = fields.Char(
        required=True, )
    brand = fields.Char()
    type = fields.Char()
    vehicle_number = fields.Char()
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Owner', ondelete='set null')
    parking_time = fields.Float()
    photo = fields.Image()
