from odoo.addons.graphql_base import OdooObjectType
from graphene import String, Int, DateTime, List, InputObjectType
from ..types.parcel import Parcel, InputParcel


class Farm(OdooObjectType):
    id = Int()
    name = String()
    create_date = DateTime()
    description = String()
    code = String()
    partner_id = Int()
    parcels = List(Parcel)

    @staticmethod
    def resolve_parcels(root, info):
        return root.parcel_ids or None


class InputFarm(InputObjectType):
    name = String()
    description = String()
    code = String()
    partner_id = Int()
    parcels = List(InputParcel)
