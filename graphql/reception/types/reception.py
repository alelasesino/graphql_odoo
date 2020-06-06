from odoo.addons.graphql_base import OdooObjectType
from graphene import InputObjectType, String, Int, Float, DateTime, List
from ...product.types.product import InputProduct


class ProductReception(OdooObjectType):
    id = Int()
    code = String()
    display_name = String()
    kilos = Float()
    lote = String()

    @staticmethod
    def resolve_id(root, info):
        return root.product_id.id

    @staticmethod
    def resolve_code(root, info):
        return root.product_id.code

    @staticmethod
    def resolve_kilos(root, info):
        return root.qty_done

    @staticmethod
    def resolve_lote(root, info):
        return root.lot_id.name


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

        # Se comprueba si la recepcion solicitada 
        # no lleva un filtrado por lotes
        if not 'args' in info.context:
            return products
        return filter(lambda product: product.lot_id.name == info.context["args"]["lot_filter"], products)


class InputReception(InputObjectType):
    farm_id = Int(required=True)
    products = List(InputProduct)