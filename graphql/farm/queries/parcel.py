from graphene import Int
from ... import FieldResolver
from ..types.parcel import Parcel


class ParcelQuery(FieldResolver):
    class Arguments:
        id = Int(required=True)

    Output = Parcel

    def resolve(self, info, id):
        return info.context["env"]["agro.farm.parcel"].search([('id', '=', id)]) or None