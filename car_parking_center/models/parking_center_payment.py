from odoo import _, api, exceptions, fields, models


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
    state = fields.Selection(
        selection=[('reserved', _('Reserved')),
                   ('parked', _('Parked')),
                   ('left', _('Left'))],
        related='visit_id.state',
        store=False,
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

    @api.constrains('amount', 'visit_id')
    def constrains_amount(self):
        for record in self:
            total_amount = 0
            for payment in self.env['parking.center.payment'].search([('visit_id', '=', record.visit_id.id)]):
                total_amount += payment.amount
            if total_amount > record.visit_id.amount:
                raise exceptions.UserError(
                    _("Total amount of payments ({:.2f}) should not exceed the parking visit amount ({:.2f})")
                    .format(total_amount, record.visit_id.amount))
            if total_amount < record.visit_id.amount and record.visit_id.state == 'left':
                raise exceptions.UserError(
                    _("Car has left the parking. You cannot reduce the payment amount"))

    @api.ondelete(at_uninstall=False)
    def _unlink_only_if_not_left(self):
        for record in self:
            if record.visit_id.state == 'left':
                raise exceptions.UserError(
                    _("Car has left the parking. You cannot remove/deactivate the payment"))
