from odoo.addons.graphql_base import OdooObjectType
from graphene import String, Int, Float


class Product(OdooObjectType):
    id = Int()
    display_name = String()
    name = String()
    code = String()
    image = String()
    weight = Float()
    uom = String()

    @staticmethod
    def resolve_image(root, info):
        if root.image_128:
            return root.image_128.decode("utf-8")
        return ""

    @staticmethod
    def resolve_uom(root, info):
        return "Cajas" if root.uom_name == "Unidades" else root.uom_name
