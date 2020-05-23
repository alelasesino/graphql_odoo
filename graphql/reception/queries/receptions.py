from graphene import List, Boolean
from ... import FieldResolver
from ..types.reception import Reception
from ...utils import utc_to_local, today_datetime_start, today_datetime_end


class ReceptionsQuery(FieldResolver):
    class Arguments:
        today = Boolean(default_value=True)
    
    Output = List(Reception)

    def resolve(self, info, today):
        domain = []
        if today:
            domain.append(('scheduled_date', '>=', today_datetime_start()))
            domain.append(('scheduled_date', '<=', today_datetime_end()))

        return info.context["env"]["stock.picking"].search(domain)
        