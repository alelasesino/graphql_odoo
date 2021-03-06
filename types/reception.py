from odoo.addons.graphql_base import OdooObjectType
from graphene import InputObjectType, Int, Float, List, String, Field
from .product import Product
from .parcel import Parcel


class InputStockMoveLine(InputObjectType):
    product_id = Int()
    parcel_id = Int()
    quantity = Float()


class Location(OdooObjectType):
    id = Int()
    parcel_id = Field(Parcel)
    name = String()
    parent_name = String()
    complete_name = String()

    @staticmethod
    def resolve_parent_name(root, info):
        return root.location_id.name


class ReceptionLine(OdooObjectType):
    id = Int()
    product_id = Field(Product)
    location_id = Field(Location)
    lot = String()
    quantity = Float()

    @staticmethod
    def resolve_quantity(root, info):
        return root.qty_done

    @staticmethod
    def resolve_lot(root, info):
        if root.lot_id:
            return root.lot_id.name
        return ""


class Reception(OdooObjectType):
    id = Int()
    name = String()
    time = String()
    state = String()
    lines = List(ReceptionLine)

    @staticmethod
    def resolve_time(root, info):
        return root.scheduled_date.strftime("%H:%M")

    @staticmethod
    def resolve_lines(root, info):
        return root.move_line_ids_without_package
