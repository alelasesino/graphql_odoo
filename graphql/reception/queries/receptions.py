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
            # Se filtran las recepciones por un lote espeficado y 
            # se guarda dicho lote en el contexto 'args' para posteriormente 
            # filtrar los productos de dicha recepcion por el lote
            info.context["args"] = {'lot_filter': lot}
            # domain.append(('lot_id.name', '=', lot))

        if today:
            # Se filtran las recepciones a las recepciones 
            # registradas en el dia de hoy
            domain.append(('picking_id.scheduled_date', '>=', today_datetime_start()))
            domain.append(('picking_id.scheduled_date', '<=', today_datetime_end()))

        return info.context["env"]["stock.move.line"].search(domain).picking_id     