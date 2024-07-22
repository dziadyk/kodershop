
from odoo import _, fields, models


class Visit(models.Model):
    _name = 'parking.center.visit'
    _description = 'Visit'

    active = fields.Boolean(
        default=True, )
    name = fields.Char(
        required=True, )
    type = fields.Selection(
        selection=[('reserved', _('Reserved')),
                   ('parked', _('Parked')),
                   ('left', _('Left'))],
        required=True, default='parked', )
    car_id = fields.Many2one(
        comodel_name='parking.center.car',
        string='Car', ondelete='restrict')
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Car Owner', ondelete='set null')
    parking_time = fields.Float()
    amount = fields.Float(
        required=True, digits=(10, 2))
    payment_ids = fields.One2many(
        comodel_name='parking.center.payment',
        inverse_name='visit_id')
