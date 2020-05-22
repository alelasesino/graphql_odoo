import graphene
from odoo import _
from odoo.exceptions import UserError
from odoo.addons.graphql_base import OdooObjectType

from .farm.queries.farm import FarmQuery
from .farm.queries.farms import FarmsQuery

from .farm.queries.parcel import ParcelQuery
from .farm.queries.parcels import ParcelsQuery

from .reception.queries.reception import ReceptionQuery
from .reception.queries.receptions import ReceptionsQuery

from .product.queries.product import ProductQuery
from .product.queries.products import ProductsQuery

class Country(OdooObjectType):
    code = graphene.String(required=True)
    name = graphene.String(required=True)


class Partner(OdooObjectType):
    name = graphene.String(required=True)
    street = graphene.String()
    street2 = graphene.String()
    city = graphene.String()
    zip = graphene.String()
    country = graphene.Field(Country)
    email = graphene.String()
    phone = graphene.String()
    is_company = graphene.Boolean(required=True)
    contacts = graphene.List(graphene.NonNull(lambda: Partner), required=True)

    @staticmethod
    def resolve_country(root, info):
        return root.country_id or None

    @staticmethod
    def resolve_contacts(root, info):
        return root.child_ids


class Query(graphene.ObjectType):

    farms = FarmsQuery.Field()
    farm = FarmQuery.Field()

    parcels = ParcelsQuery.Field()
    parcel = ParcelQuery.Field()

    receptions = ReceptionsQuery.Field()
    reception = ReceptionQuery.Field()

    products = ProductsQuery.Field()
    product = ProductQuery.Field()

    all_partners = graphene.List(
        graphene.NonNull(Partner),
        required=True,
        companies_only=graphene.Boolean(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    reverse = graphene.String(
        required=True,
        description="Reverse a string",
        word=graphene.String(required=True),
    )

    error_example = graphene.String()

    @staticmethod
    def resolve_all_partners(root, info, companies_only=False, limit=None, offset=None):
        domain = []
        if companies_only:
            domain.append(("is_company", "=", True))
        return info.context["env"]["res.partner"].search(
            domain, limit=limit, offset=offset
        )

    @staticmethod
    def resolve_reverse(root, info, word):
        return word[::-1]

    @staticmethod
    def resolve_error_example(root, info):
        raise UserError(_("UserError example"))


class CreatePartner(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        is_company = graphene.Boolean()
        raise_after_create = graphene.Boolean()

    Output = Partner

    @staticmethod
    def mutate(self, info, name, email, is_company=False, raise_after_create=False):
        env = info.context["env"]
        partner = env["res.partner"].create(
            {"name": name, "email": email, "is_company": is_company}
        )
        if raise_after_create:
            raise UserError(_("as requested"))
        return partner


class Mutation(graphene.ObjectType):
    create_partner = CreatePartner.Field(description="Documentation of CreatePartner")


schema = graphene.Schema(query=Query, mutation=Mutation)
