from odoo import _, api, exceptions, fields, models


class Visit(models.Model):
    _name = 'parking.center.visit'
    _description = 'Parking Visit'

    name = fields.Char(
        compute='_compute_name',
        store=True,
    )
    date = fields.Date(
        default=lambda self: fields.Datetime.today(),
        required=True,
    )
    lot_number = fields.Integer(
        string='Lot number',
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
        inverse_name='visit_id',
    )
    paid = fields.Boolean(
        compute='_compute_paid',
        store=False,
    )

    @api.constrains('lot_number', 'car_id', 'state')
    def constrains_lot_number(self):
        for record in self:
            if record.lot_number <= 0 and record.state != 'reserved':
                raise exceptions.UserError(
                    _("Lot number can't be 0"))
            if record.lot_number > 100:
                raise exceptions.UserError(
                    _("Parking center have only 100 lot numbers"))
            if record.state == 'parked':
                if self.env['parking.center.visit'].search_count([('state', '=', 'parked'),
                                                                  ('lot_number', '=', record.lot_number),
                                                                  ('id', '!=', record.id)]):
                    raise exceptions.UserError(
                        _("Parking lot {} is currently occupied").format(record.lot_number))
                if self.env['parking.center.visit'].search_count([('state', '=', 'parked'),
                                                                  ('car_id', '=', record.car_id.id),
                                                                  ('id', '!=', record.id)]):
                    raise exceptions.UserError(
                        _("{} is parked now. You cannot create one more visit").format(record.car_id.name))

    @api.constrains('amount')
    def constrains_amount(self):
        for record in self:
            if record.amount <= 0:
                raise exceptions.UserError(
                    _("Visit amount must be greater than 0.00"))

    @api.constrains('state')
    def constrains_state(self):
        for record in self:
            if record.state == 'left' and not record.paid:
                raise exceptions.UserError(
                    _("The car can't leave parking center. Payment amount doesn't equal visit amount"))

    @api.depends('date', 'lot_number', 'car_id')
    def _compute_name(self):
        for record in self:
            record.name = ''
            if record.lot_number:
                record.name += '{}'.format(record.lot_number) + ' '
            if record.car_id:
                record.name += record.car_id.name + ' '
            if record.date:
                record.name += record.date.strftime("%m/%d/%Y")

    @api.depends('amount', 'payment_ids')
    def _compute_paid(self):
        for record in self:
            if record.amount == 0:
                record.paid = False
                break
            payment_amount = 0
            for payment in record.payment_ids:
                payment_amount += payment.amount
            record.paid = record.amount == payment_amount
