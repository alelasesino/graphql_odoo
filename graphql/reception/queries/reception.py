from graphene import Int
from ... import FieldResolver
from ..types.reception import Reception
from odoo.exceptions import UserError
from odoo import _


class ReceptionQuery(FieldResolver):
    class Arguments:
        id = Int(required=True)

    Output = Reception

    def resolve(self, info, id):
        reception = info.context["env"]["stock.picking"].search([('id', '=', id)])
        if reception:
            return reception
        raise UserError(_(f"Reception with ID: {id} not exist!"))