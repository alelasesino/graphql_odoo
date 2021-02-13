from odoo.addons.graphql_base import OdooObjectType
from graphene import Int, String, Field, List, DateTime, Float
from .product import Product
from .reception import Location
from .partner import Partner
from .cmr import Cmr


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
    palets = List(lambda: Palet)
    cmr_id = Field(Cmr)

    @staticmethod
    def resolve_state(root, info):
        return "sold" if root.delivery_state == "done" else root.state

    @staticmethod
    def resolve_order_lines(root, info):
        return root.order_line

    @staticmethod
    def resolve_palets(root, info):
        return root.palet_ids.sorted('name', reverse=True)

    @staticmethod
    def resolve_cmr_id(root, info):
        return root.cmr_ids


from .palet import Palet
