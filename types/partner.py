from odoo.addons.graphql_base import OdooObjectType
from graphene import Int, String, Field


class Partner(OdooObjectType):
    id = Int()
    name = String()
    city = String()
    country = String()
    image = String()
    color = String()
    sale_order_count = Int()
    purchase_order_count = Int()
    parent_id = Field(lambda: Partner)

    @staticmethod
    def resolve_country(root, info):
        return root.country_id.name if root.country_id.name else ""

    @staticmethod
    def resolve_image(root, info):
        return root.image_128.decode("utf-8") if root.image_128 else ""

    @staticmethod
    def resolve_color(root, info):
        return root.colour if root.colour else ""
