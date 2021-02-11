
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    colour = fields.Char(string="Color")
