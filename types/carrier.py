from odoo.addons.graphql_base import OdooObjectType
from graphene import InputObjectType, Int, String


class InputCarrierCompany(InputObjectType):
    name = String(required=True)
    nif = String()


class CarrierCompany(OdooObjectType):
    id = Int()
    name = String()
    nif = String()
