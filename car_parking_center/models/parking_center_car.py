
from odoo import _, api, fields, models


class Car(models.Model):
    _name = 'parking.center.car'
    _description = 'Car'

    name = fields.Char(
        compute='_compute_name',
        store=True,
    )
    brand = fields.Char(
        required=True,
    )
    model = fields.Char()
    vehicle_number = fields.Char(
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Owner',
        ondelete='set null',
    )
    photo = fields.Image()
    visit_ids = fields.One2many(
        comodel_name='parking.center.visit',
        inverse_name='car_id',
    )
    visit_count = fields.Integer(
        string='Times in parking center',
        compute='_compute_visit_count',
        store=False,
    )
    state = fields.Selection(
        selection=[('new', _('New')),
                   ('reserved', _('Reserved')),
                   ('parked', _('Parked')),
                   ('left', _('Left'))],
        compute='_compute_state',
        default='new',
        store=False,
    )

    @api.depends('brand', 'model', 'vehicle_number')
    def _compute_name(self):
        for record in self:
            record.name = (record.brand or '') + ' ' + (record.model or '') + ' ' + (record.vehicle_number or '')

    @api.depends('visit_ids')
    def _compute_visit_count(self):
        for record in self:
            record.visit_count = self.env['parking.center.visit'].search_count([('car_id', '=', record.id)])

    @api.depends('visit_ids')
    def _compute_state(self):
        for record in self:
            record.state = 'new'
            for visit in record.visit_ids:
                record.state = 'left'
                if visit.state == 'parked':
                    record.state = 'parked'
                    break
                if visit.state == 'reserved':
                    record.state = 'reserved'
