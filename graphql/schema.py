from importlib import import_module
from logging import getLogger
from graphene import Schema, ObjectType

_logger = getLogger(__name__)


def obtain_schema(modules) -> Schema:
    queries = []
    mutations = []
    for module in modules:
        try:
            query = getattr(import_module(
                f"odoo.addons.{module.name}"), "Query")
            queries.append(query)
        except (ImportError, AttributeError) as e:
            _logger.warning(f"Can't import queries from {module.name}!")

        try:
            mutation = getattr(import_module(
                f"odoo.addons.{module.name}"), "Mutation")
            mutations.append(mutation)
        except (ImportError, AttributeError) as e:
            _logger.warning(f"Can't import mutations from {module.name}!")

    queries.append(ObjectType)
    mutations.append(ObjectType)

    Query = type('Query', tuple(queries), {})
    Mutation = type('Mutation', tuple(mutations), {})
    options = {}

    if len(queries) > 1:
        options["query"] = Query

    if len(mutations) > 1:
        options["mutation"] = Mutation

    return Schema(**options)
