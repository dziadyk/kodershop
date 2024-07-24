
from odoo import _, api, fields, models


class Payment(models.Model):
    _name = 'parking.center.payment'
    _description = 'Payment'

    name = fields.Char(
        compute='_compute_name',
        store=True,
    )
    date = fields.Datetime(
        default=lambda self: fields.Datetime.now(),
        required=True,
    )
    type = fields.Selection(
        selection=[('card', _('Card')),
                   ('cash', _('Cash'))],
        default='card',
        required=True,
    )
    amount = fields.Float(
        digits=(10, 2),
        required=True,
    )
    visit_id = fields.Many2one(
        string='Parking Visit',
        comodel_name='parking.center.visit',
        ondelete='cascade',
        required=True,
    )
    car_id = fields.Many2one(
        string='Car',
        related='visit_id.car_id',
        store=True,
        readonly=True,
    )
    partner_id = fields.Many2one(
        string='Owner',
        related='visit_id.partner_id',
        store=True,
        readonly=True,
    )

    @api.depends('date', 'type', 'amount')
    def _compute_name(self):
        for record in self:
            record.name = 'Payment '
            if record.amount:
                record.name += '{:.2f}'.format(record.amount) + ' '
            if record.type:
                record.name += record.type.capitalize() + ' '
            if record.date:
                record.name += record.date.strftime("%m/%d/%Y %H:%M:%S")
