from odoo.addons.graphql_base import OdooObjectType
from graphene import String, Int, Float, List


class Product(OdooObjectType):
    id = Int()
    display_name = String()
    name = String()
    code = String()
    image = String()
    color = String()
    weight = Float()
    uom = String()
    tracking = String()
    produce_products = List(lambda: Product)

    @staticmethod
    def resolve_image(root, info):
        if root.image_128:
            return root.image_128.decode("utf-8")
        return ""

    @staticmethod
    def resolve_color(root, info):
        return root.product_tmpl_id.colour if root.product_tmpl_id.colour else ""

    @staticmethod
    def resolve_uom(root, info):
        return "Cajas" if root.uom_name == "Unidades" else root.uom_name

    @staticmethod
    def resolve_produce_products(root, info):
        env = info.context["env"]
        bom_ids = env['mrp.bom'].search([('bom_line_ids.product_id', '=', root.id)])
        return bom_ids.mapped("product_id")
