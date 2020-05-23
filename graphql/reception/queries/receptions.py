import datetime
from graphene import List, Boolean
from ... import FieldResolver
from ..types.reception import Reception
from ...utils import utc_to_local


class ReceptionsQuery(FieldResolver):
    class Arguments:
        today = Boolean(default_value=True)

    Output = List(Reception)

    def resolve(self, info, today):

        all_receptions = info.context["env"]["stock.picking"].search([])
        
        if today:
            receptions = []
            for reception in all_receptions:
                scheduled_date=utc_to_local(reception.scheduled_date)

                if datetime.datetime.today().day == scheduled_date.day:
                    receptions.append(reception)

            return receptions

        return all_receptions