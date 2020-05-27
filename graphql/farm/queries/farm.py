from graphene import Int
from ... import FieldResolver
from ..types.farm import Farm
from odoo.exceptions import UserError
from odoo import _


class FarmQuery(FieldResolver):
    class Arguments:
        id = Int(required=True)

    Output = Farm

    def resolve(self, info, id):
        farm = info.context["env"]["agro.farm"].search([('id', '=', id)])
        if farm:
            return farm
        raise UserError(_(f"Farm with ID: {id} not exist!"))