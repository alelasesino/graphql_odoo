from graphene import Int
from ... import FieldResolver
from ..types.farm import Farm


class FarmQuery(FieldResolver):
    class Arguments:
        id = Int(required=True)

    Output = Farm

    def resolve(self, info, id):
        return info.context["env"]["agro.farm"].search([('id', '=', id)]) or None