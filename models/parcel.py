
from odoo import models, fields


class Parcel(models.Model):
    _inherit = 'agro.farm.parcel'

    color = fields.Char(string="Color")
