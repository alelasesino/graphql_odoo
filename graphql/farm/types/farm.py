from graphene import ObjectType, String, Int, DateTime, List
from ..types.parcel import Parcel 


class Farm(ObjectType):
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