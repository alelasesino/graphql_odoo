from graphene import Schema, ObjectType 
from odoo import _
from odoo.addons.graphql_base import OdooObjectType

from .farm.queries.farm import FarmQuery
from .farm.queries.farms import FarmsQuery
from .farm.mutations.farm import CreateFarm, RemoveFarm

from .farm.queries.parcel import ParcelQuery
from .farm.queries.parcels import ParcelsQuery

from .reception.queries.reception import ReceptionQuery
from .reception.queries.receptions import ReceptionsQuery
from .reception.mutations.reception import CreateReception

from .product.queries.product import ProductQuery
from .product.queries.products import ProductsQuery


class Query(ObjectType):

    farms = FarmsQuery.Field()
    farm = FarmQuery.Field()

    parcels = ParcelsQuery.Field()
    parcel = ParcelQuery.Field()

    receptions = ReceptionsQuery.Field()
    reception = ReceptionQuery.Field()

    products = ProductsQuery.Field()
    product = ProductQuery.Field()


class Mutation(ObjectType):
    create_farm = CreateFarm.Field()
    remove_farm = RemoveFarm.Field()

    create_reception = CreateReception.Field()


schema = Schema(query=Query, mutation=Mutation)
