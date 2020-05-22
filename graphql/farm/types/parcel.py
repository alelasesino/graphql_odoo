from graphene import ObjectType, String, Int, DateTime, List, Float


class Parcel(ObjectType):
    id = Int()
    name = String()
    create_date = DateTime()
    number = Int()
    description = String()