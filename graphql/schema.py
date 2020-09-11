from graphene import Schema, ObjectType


class Query(ObjectType):
    pass


class Mutation(ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
