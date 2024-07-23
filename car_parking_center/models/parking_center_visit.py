
from odoo import _, fields, models
from datetime import datetime


class Visit(models.Model):
    _name = 'parking.center.visit'
    _description = 'Visit'

    active = fields.Boolean(
        default=True,
    )
    name = fields.Char(
        required=True,
    )
    date = fields.Datetime(
        default=lambda self: fields.Datetime.now(),
        required=True,
    )
    lot_number = fields.Integer(
        string='Parking lot number',
    )
    state = fields.Selection(
        selection=[('reserved', _('Reserved')),
                   ('parked', _('Parked')),
                   ('left', _('Left'))],
        default='parked',
        required=True,
    )
    car_id = fields.Many2one(
        comodel_name='parking.center.car',
        string='Car',
        ondelete='restrict',
    )
    partner_id = fields.Many2one(
        string='Car Owner',
        related='car_id.partner_id',
        store=True,
        readonly=True,
    )
    parking_time = fields.Float(
        string='Time',
    )
    amount = fields.Float(
        digits=(10, 2),
        required=True,
    )
    payment_ids = fields.One2many(
        comodel_name='parking.center.payment',
        inverse_name='visit_id')
