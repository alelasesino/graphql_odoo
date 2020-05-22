from graphene import List
from ... import FieldResolver
from ..types.parcel import Parcel

class ParcelsQuery(FieldResolver):

    Output = List(Parcel)

    def resolve(self, info):
        return info.context["env"]["agro.farm.parcel"].search([])