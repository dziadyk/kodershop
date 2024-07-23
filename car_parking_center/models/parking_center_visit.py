
from odoo import _, api, fields, models


class Visit(models.Model):
    _name = 'parking.center.visit'
    _description = 'Visit'

    active = fields.Boolean(
        default=True,
    )
    name = fields.Char(
        compute='_compute_name',
        store=True,
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
        string='Car',
        comodel_name='parking.center.car',
        ondelete='restrict',
        required=True,
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

    @api.depends('date', 'lot_number', 'car_id')
    def _compute_name(self):
        for record in self:
            record.name = ''
            if record.lot_number:
                record.name += '{}'.format(record.lot_number) + ' '
            if record.car_id:
                record.name += record.car_id.name + ' '
            if record.date:
                record.name += record.date.strftime("%m/%d/%Y %H:%M:%S")