from odoo.addons.graphql_base import OdooObjectType
from graphene import InputObjectType, Int, String, Field, List, Float
from .product import Product
from .reception import Location
from .partner import Partner
from .sale import SaleOrder


class InputPaletLine(InputObjectType):
    move_line_id = Int()
    kilos = Float()
    quantity = Int()
    produce_product = Int()


class PaletLine(OdooObjectType):
    id = Int()
    product_id = Field(Product)
    location_id = Field(Location)
    lot = String()
    quantity = Int()
    kilos = Float()
    uom = String()

    @staticmethod
    def resolve_product_id(root, info):
        return root.produce_product_id

    @staticmethod
    def resolve_lot(root, info):
        return root.lot_id.name

    @staticmethod
    def resolve_uom(root, info):
        return "Cajas" if root.produce_product_id.uom_id.name == "Unidades" else root.product_uom_id.name


class Palet(OdooObjectType):
    id = Int()
    name = String()
    code = String()
    partner_id = Field(Partner)
    destiny_partner_id = Field(Partner)
    total_quantity = Int()
    total_kilos = Float()
    lines = List(PaletLine)
    state = String()
    order_id = Field(SaleOrder)

    @staticmethod
    def resolve_total_quantity(root, info):
        return sum([line.quantity for line in root.palet_line_ids])

    @staticmethod
    def resolve_total_kilos(root, info):
        return sum([line.kilos for line in root.palet_line_ids])

    @staticmethod
    def resolve_lines(root, info):
        return root.palet_line_ids
