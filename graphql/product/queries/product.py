from graphene import Int
from ... import FieldResolver
from ..types.product import Product


class ProductQuery(FieldResolver):
    class Arguments:
        id = Int(required=True)

    Output = Product

    def resolve(self, info, id):
        return info.context["env"]["product.product"].search([('id', '=', id)]) or None