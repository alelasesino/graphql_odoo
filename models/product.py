
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    colour = fields.Char(string="Color")
