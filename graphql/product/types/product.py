from odoo.addons.graphql_base import OdooObjectType
from graphene import String, Int


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