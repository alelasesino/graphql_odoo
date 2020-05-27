from graphene import Int
from ... import FieldResolver
from ..types.parcel import Parcel
from odoo.exceptions import UserError
from odoo import _


class ParcelQuery(FieldResolver):
    class Arguments:
        id = Int(required=True)

    Output = Parcel

    def resolve(self, info, id):
        parcel = info.context["env"]["agro.farm.parcel"].search([('id', '=', id)])
        if parcel:
            return parcel
        raise UserError(_(f"Parcel with ID: {id} not exist!"))