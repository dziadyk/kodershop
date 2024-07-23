
from odoo import _, api, fields, models
from datetime import datetime

class Payment(models.Model):
    _name = 'parking.center.payment'
    _description = 'Payment'

    active = fields.Boolean(
        default=True)
    name = fields.Char(
        compute='_compute_name',
        store=True)
    date = fields.Datetime(
        required=True,
        default=lambda self: fields.Datetime.now())
    type = fields.Selection(
        selection=[('card', _('Card')),
                   ('cash', _('Cash'))],
        required=True, default='card', )
    amount = fields.Float(
        required=True, digits=(10, 2))
    visit_id = fields.Many2one(
        comodel_name='parking.center.visit',
        string='Parking Visit',
        required=True, ondelete='cascade')
    car_id = fields.Many2one(related='visit_id.car_id', string='Car', store=True, readonly=True)
    partner_id = fields.Many2one(related='visit_id.partner_id', string='Owner', store=True, readonly=True)

    @api.depends('date', 'type', 'amount')
    def _compute_name(self):
        for record in self:
            record.name = 'Payment '
            if record.amount:
                record.name += str(record.amount) + ' '
            if record.type:
                record.name += record.type.capitalize() + ' '
            if record.date:
                record.name += record.date.strftime("%m/%d/%Y %H:%M:%S")
