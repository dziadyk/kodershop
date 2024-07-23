
from odoo import _, fields, models
from datetime import datetime


class Visit(models.Model):
    _name = 'parking.center.visit'
    _description = 'Visit'

    active = fields.Boolean(
        default=True)
    name = fields.Char(
        required=True)
    date = fields.Datetime(
        required=True,
        default=lambda self: fields.Datetime.now())
    lot_number = fields.Integer(
        string='Parking lot number', )
    state = fields.Selection(
        selection=[('reserved', _('Reserved')),
                   ('parked', _('Parked')),
                   ('left', _('Left'))],
        required=True, default='parked', )
    car_id = fields.Many2one(
        comodel_name='parking.center.car',
        string='Car', ondelete='restrict')
    partner_id = fields.Many2one(
        related='car_id.partner_id',
        string='Car Owner',
        store=True, readonly=True)
    parking_time = fields.Float(
        string='Time')
    amount = fields.Float(
        required=True, digits=(10, 2))
    payment_ids = fields.One2many(
        comodel_name='parking.center.payment',
        inverse_name='visit_id')
