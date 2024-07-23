
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
    vehicle_number = fields.Char(
        required=True,
    )
    type = fields.Char()
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Owner',
        ondelete='set null',
    )
    parking_count = fields.Float(
        string='Times in parking center',
        compute='_compute_parking_count',
        store=False,
    )
    photo = fields.Image()
    visit_ids = fields.One2many(
        comodel_name='parking.center.visit',
        inverse_name='car_id',
    )

    @api.depends('brand', 'vehicle_number')
    def _compute_name(self):
        for record in self:
            record.name = (record.brand or '') + ' ' + (record.vehicle_number or '')
