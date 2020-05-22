from graphene import List
from ... import FieldResolver
from ..types.reception import Reception


class ReceptionsQuery(FieldResolver):

    Output = List(Reception)

    def resolve(self, info):
        return info.context["env"]["stock.picking"].search([])