from odoo.http import Controller, route, request
from odoo.addons.graphql_base import GraphQLControllerMixin
from ..graphql.schema import obtain_schema


GRAPHQL_MODULES = ["graphql_stock", "graphql_mrp", "graphql_sale", "graphql_purchase"]


class GraphQLController(Controller, GraphQLControllerMixin):

    # The GraphiQL route, providing an IDE for developers
    # @route("/graphiql", auth="user")
    # def graphiql(self, **kwargs):
    #     return self._handle_graphiql_request(obtain_schema(self.__obtain_modules_installed()))

    # Optional monkey patch, needed to accept application/json GraphQL
    # requests. If you only need to accept GET requests or POST
    # with application/x-www-form-urlencoded content,
    # this is not necessary.
    GraphQLControllerMixin.patch_for_json("^/graphql/?$")

    # The graphql route, for applications.
    # Note csrf=False: you may want to apply extra security
    # (such as origin restrictions) to this route.
    @route("/graphql", auth="user", csrf=False)
    def graphql(self, **kwargs):
        return self._handle_graphql_request(obtain_schema(self.__obtain_modules_installed()))

    # Obtain modules installed related graphql
    # that contains queries and mutations for the schema
    def __obtain_modules_installed(self):
        domain = [('name', 'in', GRAPHQL_MODULES), ('state', '=', 'installed')]
        modules_installed = request.env['ir.module.module'].search(domain)
        return modules_installed
