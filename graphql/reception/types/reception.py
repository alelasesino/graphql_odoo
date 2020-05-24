from odoo.addons.graphql_base import OdooObjectType
from graphene import InputObjectType, String, Int, DateTime, List
from .product_reception import ProductReception
from ...product.types.product import InputProduct


class Reception(OdooObjectType):
    id = Int()
    display_name = String()
    scheduled_date = DateTime()
    receive_from = Int()
    time = String()
    receive_products = List(ProductReception)

    @staticmethod
    def resolve_receive_from(root, info):
        return root.location_id.id

    @staticmethod
    def resolve_time(root, info):
        return root.scheduled_date.strftime("%H:%M")

    @staticmethod
    def resolve_receive_products(root, info):
        products = root.move_ids_without_package.move_line_nosuggest_ids
        if not 'args' in info.context:
            return products
        return filter(lambda product: product.lot_id.name == info.context["args"]["lot_filter"], products)


class InputReception(InputObjectType):
    farm_id = Int()
    products = List(InputProduct)