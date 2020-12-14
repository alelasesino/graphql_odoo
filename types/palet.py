from odoo.addons.graphql_base import OdooObjectType
from graphene import InputObjectType, Int, String, Field, List
from .product import Product
from .reception import Location
from .partner import Partner


class InputPaletLine(InputObjectType):
    move_line_id = Int()
    kilos = Int()
    quantity = Int()


class PaletLine(OdooObjectType):
    id = Int()
    product_id = Field(Product)
    location_id = Field(Location)
    lot = String()
    quantity = Int()
    kilos = Int()
    uom = String()

    @staticmethod
    def resolve_lot(root, info):
        return root.lot_id.name

    @staticmethod
    def resolve_uom(root, info):
        return "Cajas" if root.product_uom_id.name == "Unidades" else root.product_uom_id.name


class Palet(OdooObjectType):
    id = Int()
    name = String()
    code = String()
    partner_id = Field(Partner)
    total_quantity = Int()
    total_kilos = Int()
    lines = List(PaletLine)
    state = String()
    sale_state = String()

    @staticmethod
    def resolve_total_quantity(root, info):
        return sum([line.quantity for line in root.palet_line_ids])

    @staticmethod
    def resolve_total_kilos(root, info):
        return sum([line.kilos for line in root.palet_line_ids])

    @staticmethod
    def resolve_lines(root, info):
        return root.palet_line_ids
