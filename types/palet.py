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
    zpl = String()
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

    @staticmethod
    def resolve_zpl(root, info):
        lines = []
        partner = {}
        palet_ezpl = root.env['ir.config_parameter'].get_param('agro_stock.palet_ezpl')

        def get_safe_partner_field(field, *args):
            if not root.partner_id:
                return ""
            if field == "country_id":
                return root.partner_id[field][args[0]].upper() if root.partner_id[field][args[0]] else ""
            return root.partner_id[field].upper() if root.partner_id[field] else ""

        def get_barcode_128(weight):
            return f"21{root.id:05}&G3102{weight*100:06}"

        for i in range(3):
            quantity = int(root.palet_line_ids[i].quantity) if len(root.palet_line_ids) > i else ""
            description = root.palet_line_ids[i].produce_product_id.code if len(root.palet_line_ids) > i else ""
            lines.append({"quantity": quantity, "description": description})

        weight = int(sum([line.kilos for line in root.palet_line_ids]))
        quantity = int(sum([line.quantity for line in root.palet_line_ids]))

        return palet_ezpl.format(
            barcode=get_barcode_128(weight),
            code=root.code,
            ref=root.name,
            quantity=quantity,
            weight=weight,
            order=root.order_id.name or "",
            line1=f"VC,383,1173,1,1,0,3E,{lines[0]['quantity']} X {lines[0]['description']}" if lines[0]['quantity'] != "" else "",
            line2=f"\nVC,474,1173,1,1,0,3E,{lines[1]['quantity']} X {lines[1]['description']}" if lines[1]['quantity'] != "" else "",
            line3=f"\nVC,429,1173,1,1,0,3E,{lines[2]['quantity']} X {lines[2]['description']}" if lines[2]['quantity'] != "" else "",
            customer=get_safe_partner_field("name"),
            street=get_safe_partner_field("street"),
            zip=get_safe_partner_field("zip"),
            city=get_safe_partner_field("city"),
            country=get_safe_partner_field("country_id", "code"),
            phone=get_safe_partner_field("phone"),
        )
