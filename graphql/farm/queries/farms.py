from graphene import List
from ... import FieldResolver
from ..types.farm import Farm

class FarmsQuery(FieldResolver):

    Output = List(Farm)

    def resolve(self, info):
        return info.context["env"]["agro.farm"].search([])