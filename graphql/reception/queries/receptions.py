from graphene import List, Boolean, String
from ... import FieldResolver
from ..types.reception import Reception
from ...utils import utc_to_local, today_datetime_start, today_datetime_end


class ReceptionsQuery(FieldResolver):
    class Arguments:
        today = Boolean(default_value=True)
        lot = String()
    
    Output = List(Reception)

    def resolve(self, info, today, lot=None):
        domain = []

        if lot:
            info.context["args"] = {'lot_filter': lot}
            domain.append(('lot_id.name', '=', lot))

        if today:
            domain.append(('picking_id.scheduled_date', '>=', today_datetime_start()))
            domain.append(('picking_id.scheduled_date', '<=', today_datetime_end()))

        return info.context["env"]["stock.move.line"].search(domain).picking_id     