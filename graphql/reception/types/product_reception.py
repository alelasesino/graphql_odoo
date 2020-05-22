from odoo.addons.graphql_base import OdooObjectType
from graphene import String, Int, Float


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