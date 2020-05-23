from odoo.addons.graphql_base import OdooObjectType
from graphene import InputObjectType, String, Int, Float


class Product(OdooObjectType):
    id = Int()
    display_name = String()
    code = String()
    barcode = String()
    categ_id = Int()
    image = String()

    @staticmethod
    def resolve_image(root, info):
        return root.image_512


class InputProduct(InputObjectType):
    id = Int()
    lot = String()
    quantity = Float()