from graphene import Int
from ... import FieldResolver
from ..types.product import Product
from odoo.exceptions import UserError
from odoo import _


class ProductQuery(FieldResolver):
    class Arguments:
        id = Int(required=True)

    Output = Product

    def resolve(self, info, id):
        product = info.context["env"]["product.product"].search([('id', '=', id)])
        if product:
            return product
        raise UserError(_(f"Product with ID: {id} not exist!"))