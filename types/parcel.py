from odoo.addons.graphql_base import OdooObjectType
from graphene import Int, String, Field


class Farm(OdooObjectType):
    id = Int()
    name = String()


class Parcel(OdooObjectType):
    id = Int()
    name = String()
    # variety = String()
    farm_id = Field(Farm)
