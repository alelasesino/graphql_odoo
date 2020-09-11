from graphene import Schema, ObjectType


class Query(ObjectType):
    pass


class Mutation(ObjectType):
    pass


try:
    schema = Schema(query=Query, mutation=Mutation)
except AssertionError as e:
    schema = Schema()
