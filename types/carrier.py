from odoo.addons.graphql_base import OdooObjectType
from graphene import Int, String


class CarrierCompany(OdooObjectType):
    id = Int()
    name = String()
