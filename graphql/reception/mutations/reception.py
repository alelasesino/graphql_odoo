import datetime
from graphene import Mutation
from ..types.reception import Reception, InputReception


# Se almacena el entorno para acceder a los modelos
# de existentes en Odoo
env = None


# ID de la compañía la cual es reponsable de
# la recepción de inventario creada
company_id = None


# ID de la localización destino de los productos
# que contiene la recepción, se obtiene de la configuración 
# del modulo de Agricultura
location_dest_id = None


def get_partner_location_id(farm_id):
    # A partir de la finca se obtiene el ID de la compañía de origen
    # y la localización de origen de los productos
    farm = env["agro.farm"].browse(farm_id)
    return {"partner_id": farm.partner_id.id, "location_id": farm.partner_id.property_stock_supplier.id}


def get_or_create_lot(product_id, lot_name):
    # Se comprueba si ya existe el lote del producto,
    # en caso de no existir se crea dicho lote y se devuelve su ID
    model = env["stock.production.lot"]
    domain = [('name', '=', lot_name), ('product_id.id', '=', product_id)]
    lot = model.search(domain)

    if len(lot) > 0:
        return lot.id
    else:
        return model.create({'company_id': company_id,'name': lot_name,'product_id': product_id}).id


def get_stock_move_line(date, location, product, quantity, lot):
    # Se crea la linea del movimiento de stock en el inventario,
    # este pertece al modelo 'stock.move.line'
    line = {
            'company_id': company_id,
            'date': date,
            'location_dest_id': location_dest_id, 
            'location_id': location,
            'product_uom_id': product.uom_id.id,
            'qty_done': quantity,
            'product_id': product.id,
            'state': 'assigned'
        }

    # El producto podría no tener un seguimiento por lote
    if(lot):
        line["lot_id"] = get_or_create_lot(product.id, lot)

    return (0, 0, line)


def get_stock_move(date, location, product_id, quantity, lot):
    # Se crea el movimiento de stock en el inventario,
    # este pertece al modelo 'stock.move'
    product = env["product.product"].browse(product_id)
    move = (0, 0, {
                    'company_id': company_id, 
                    'date': date, 
                    'date_expected': date, 
                    'location_dest_id': location_dest_id, 
                    'location_id': location, 
                    'name': product.display_name,
                    'product_id': product_id,
                    'product_uom': product.uom_id.id,
                    'description_picking': product.name,
                    'picking_code': 'incoming',
                    'state': 'assigned',
                    'move_line_nosuggest_ids': [get_stock_move_line(date, location, product, quantity, lot)]
                })

    return move


class CreateReception(Mutation):
    class Arguments:
        reception = InputReception(required=True)

    Output = Reception

    @staticmethod
    def mutate(self, info, reception):

        global env
        global company_id
        global location_dest_id
        env = info.context["env"]

        # Se obtienen diferentes parametros que se encuentran 
        # almacenados en la configuración del módulo de agricultura.
        company_id = int(env["ir.config_parameter"].get_param('agro_fres.partner_id'))
        location_dest_id = int(env["ir.config_parameter"].get_param('agro_fres.location_id'))

        partner_location = get_partner_location_id(reception["farm_id"])
        today =  datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        move_ids_without_package = []
        for product in reception["products"]:
            lot = product["lot"] if "lot" in product else None
            move = get_stock_move(today, partner_location["location_id"], product["id"], product["quantity"], lot)
            move_ids_without_package.append(move)

        # Se crea la recepción de inventario, este pertenece al modulo 'stock.picking' 
        picking = {
            'location_dest_id': location_dest_id,
            'location_id': partner_location["location_id"],
            'picking_type_id': 1, # Entrega
            'partner_id': partner_location["partner_id"],
            'immediate_transfer': True,
            'priority': 0,
            'move_ids_without_package': move_ids_without_package
            }

        picking_created = env["stock.picking"].create(picking)

        # Se actualiza el picking_id creado anteriormente en las 
        # lineas de los movimientos de stock, pertenece al modelo 'stock.move.line'
        for package in picking_created.move_ids_without_package:
            for nosuggest in package.move_line_nosuggest_ids:
                nosuggest.write({'picking_id': picking_created.id})

        # Se realiza la validación de la recepción 
        # para actualizar el stock de los productos
        picking_created.button_validate()

        return picking_created