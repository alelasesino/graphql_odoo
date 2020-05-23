from graphene import List
from ... import FieldResolver
from ..types.product import Product


class ProductsQuery(FieldResolver):

    Output = List(Product)

    def resolve(self, info):
        return info.context["env"]["product.product"].search([], order='categ_id desc')