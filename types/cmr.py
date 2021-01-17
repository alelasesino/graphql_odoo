from odoo.addons.graphql_base import OdooObjectType
from graphene import InputObjectType, Int, String, Field, List, DateTime
from .partner import Partner
from .carrier import CarrierCompany


class InputCmr(InputObjectType):
    carrier_company_id = Int()
    transport_dni = String()
    trailer_plate = String()
    tractor_plate = String()
    temperature = Int()
    destiny_street = String()
    destiny_country = String()
    palet_count_received = Int()
    signature = String()


class CmrLine(OdooObjectType):
    id = Int()
    name = String()
    quantity = Int()
    ware = String()
    packaging = String()
    size = String()

    @staticmethod
    def resolve_packaging(root, info):
        return root.packaging_id.name


class Cmr(OdooObjectType):
    id = Int()
    name = String()
    partner_id = Field(Partner)
    date = DateTime()
    weight = Int()
    transport_dni = String()
    carrier_company_id = Field(CarrierCompany)
    trailer_plate = String()
    tractor_plate = String()
    temperature = Int()
    destiny_street = String()
    destiny_country = String()
    cmr_lines = List(CmrLine)
    palet_count_received = Int()
    state = String()

    @staticmethod
    def resolve_cmr_lines(root, info):
        return root.cmr_line_ids
