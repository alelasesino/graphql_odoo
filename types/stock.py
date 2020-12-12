from odoo.addons.graphql_base import OdooObjectType
from graphene import String, Int, Field
from .product import Product
from .reception import Location


class Lot(OdooObjectType):
    id = Int()
    name = String()


class StockQuant(OdooObjectType):
    id = Int()
    product_id = Field(Product)
    location_id = Field(Location)
    lot_id = Field(Lot)
    quantity = Int()
    uom = String()

    @staticmethod
    def resolve_uom(root, info):
        return "Cajas" if root.product_uom_id.name == "Unidades" else root.product_uom_id.name
