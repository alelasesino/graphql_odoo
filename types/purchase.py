from odoo.addons.graphql_base import OdooObjectType
from graphene import InputObjectType, Int, String, Field, List, DateTime, Float
from .product import Product
from .partner import Partner


class InputPurchaseOrderLine(InputObjectType):
    product_id = Int()
    lot = String()
    quantity = Float()


class InputUpdatePurchaseOrderLine(InputObjectType):
    lot = String()
    quantity = Float()


class PurchaseOrderLine(OdooObjectType):
    id = Int()
    product_id = Field(Product)
    quantity = Int()
    price_unit = Float()
    discount = Float()
    lot = String()
    uom = String()

    @staticmethod
    def resolve_quantity(root, info):
        return root.product_qty

    @staticmethod
    def resolve_lot(root, info):
        return root.lot_name if root.lot_name else ""

    @staticmethod
    def resolve_uom(root, info):
        return root.product_uom.name


class PurchaseOrder(OdooObjectType):
    id = Int()
    name = String()
    partner_id = Field(Partner)
    partner_ref = String()
    date_order = DateTime()
    state = String()
    order_lines = List(PurchaseOrderLine)

    @staticmethod
    def resolve_state(root, info):
        return "purchased" if root.is_purchased else root.state

    @staticmethod
    def resolve_order_lines(root, info):
        return root.order_line
