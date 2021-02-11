
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    colour = fields.Char(string="Color")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    priority = fields.Integer(string="Prioridad")
