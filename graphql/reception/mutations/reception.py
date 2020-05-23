import datetime
from graphene import Mutation
from ..types.reception import Reception, InputReception


def get_partner_location_id(env, farm_id):
    farm = env["agro.farm"].browse(farm_id)
    return {"partner_id": farm.partner_id.id, "location_id": farm.partner_id.property_stock_supplier.id}


def get_or_create_lot(env, product_id, lot_name):
    model = env["stock.production.lot"]
    domain = [('name', '=', lot_name), ('product_id.id', '=', product_id)]
    lot = model.search(domain)

    if len(lot) > 0:
        return lot.id
    else:
        return model.create({'company_id': 1,'name': lot_name,'product_id': product_id}).id


def get_stock_move_line(env, date, location, product, quantity, lot):

    line = (0, 0, {
                    'company_id': 1,
                    'date': date,
                    'location_dest_id': 8, 
                    'location_id': location,
                    'product_uom_id': product.uom_id.id,
                    # 'product_uom_qty': quantity,
                    'qty_done': quantity,
                    'product_id': product.id,
                    'lot_id': get_or_create_lot(env, product.id, lot),
                    'state': 'assigned'
                    })

    return line


def get_stock_move(env, date, location, product_id, quantity, lot):

    product = env["product.product"].browse(product_id)
    move = (0, 0, {
                    'company_id': 1, 
                    'date': date, 
                    'date_expected': date, 
                    'location_dest_id': 8, 
                    'location_id': location, 
                    'name': product.display_name,
                    'product_id': product_id,
                    'product_uom': product.uom_id.id,
                    'needs_lots': 'lot' in product.tracking,
                    'description_picking': product.name,
                    'picking_code': 'incoming',
                    'state': 'assigned',
                    'move_line_nosuggest_ids': [get_stock_move_line(env, date, location, product, quantity, lot)]
                })

    return move


class CreateReception(Mutation):
    class Arguments:
        reception = InputReception(required=True)

    Output = Reception

    @staticmethod
    def mutate(self, info, reception):

        env = info.context["env"]
        partner_location = get_partner_location_id(env, reception["farm_id"])
        today =  datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        move_ids_without_package = []
        for product in reception["products"]:
            move = get_stock_move(env, today, partner_location["location_id"], product["id"], product["quantity"], product["lot"])
            move_ids_without_package.append(move)

        picking = {   #STOCK.PICKING
            'location_dest_id': 8, #WH/Stock
            'location_id': partner_location["location_id"], #Finca #1
            'picking_type_id': 1, #Entrega
            'partner_id': partner_location["partner_id"], #Finca #1
            'immediate_transfer': True,
            'priority': 0,
            'move_ids_without_package': move_ids_without_package
            }

        picking_created = env["stock.picking"].create(picking)

        for package in picking_created.move_ids_without_package:
            for nosuggest in package.move_line_nosuggest_ids:
                nosuggest.write({'picking_id': picking_created.id})

        return picking_created