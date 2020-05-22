from odoo.addons.graphql_base import OdooObjectType
from graphene import String, Int, DateTime, List, Float, InputObjectType

class Parcel(OdooObjectType):
    id = Int()
    name = String()
    create_date = DateTime()
    number = Int()
    description = String()