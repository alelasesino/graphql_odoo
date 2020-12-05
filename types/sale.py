from odoo.addons.graphql_base import OdooObjectType
from graphene import Int, String, Field, List, DateTime, Float
from .product import Product
from .fruit_reception import Location
from .palet import Palet
from .partner import Partner


class SaleOrderLine(OdooObjectType):
    id = Int()
    product_id = Field(Product)
    quantity = Int()
    kilos = Int()
    price_unit = Float()

    @staticmethod
    def resolve_quantity(root, info):
        return root.product_uom_qty

    @staticmethod
    def resolve_kilos(root, info):
        return root.kilos_total


class SaleOrder(OdooObjectType):
    id = Int()
    name = String()
    partner_id = Field(Partner)
    date_order = DateTime()
    state = String()
    order_lines = List(SaleOrderLine)
    palets = List(Palet)

    @staticmethod
    def resolve_state(root, info):
        return "sold" if root.is_sold else root.state

    @staticmethod
    def resolve_order_lines(root, info):
        return root.order_line

    @staticmethod
    def resolve_palets(root, info):
        return root.palet_ids.sorted('name', reverse=True)
