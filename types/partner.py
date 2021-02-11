from odoo.addons.graphql_base import OdooObjectType
from graphene import Int, String


class Partner(OdooObjectType):
    id = Int()
    name = String()
    city = String()
    country = String()
    image = String()
    color = String()
    customer_rank = Int()
    supplier_rank = Int()

    @staticmethod
    def resolve_city(root, info):
        if root.city:
            return root.city
        return ""

    @staticmethod
    def resolve_country(root, info):
        if root.country_id.name:
            return root.country_id.name
        return ""

    @staticmethod
    def resolve_image(root, info):
        if root.image_128:
            return root.image_128.decode("utf-8")
        return ""

    @staticmethod
    def resolve_color(root, info):
        return root.colour if root.colour else ""
