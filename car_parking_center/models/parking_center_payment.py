
from odoo import _, fields, models


class Payment(models.Model):
    _name = 'parking.center.payment'
    _description = 'Payment'

    name = fields.Char(
        required=True, )
    date = fields.Datetime(
        required=True, )
    type = fields.Selection(
        selection=[('card', _('Card')),
                   ('cash', _('Cash'))],
        required=True, default='card', )
    amount = fields.Float(
        required=True, digits=(10, 2))
    visit_id = fields.Many2one(
        comodel_name='parking.center.visit',
        string='Parking Visit', ondelete='cascade')
