from graphene import Int
from ... import FieldResolver
from ..types.reception import Reception


class ReceptionQuery(FieldResolver):
    class Arguments:
        id = Int(required=True)

    Output = Reception

    def resolve(self, info, id):
        return info.context["env"]["stock.picking"].search([('id', '=', id)]) or None