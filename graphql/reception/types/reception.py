from graphene import ObjectType, String, Int, DateTime, List
from .product_reception import ProductReception


class Reception(ObjectType):
    id = Int()
    display_name = String()
    scheduled_date = DateTime()
    receive_from = Int()
    time = String()
    receive_products = List(ProductReception)

    @staticmethod
    def resolve_receive_from(root, info):
        return root.location_id.id

    @staticmethod
    def resolve_time(root, info):
        return root.scheduled_date.strftime("%H:%M")

    @staticmethod
    def resolve_receive_products(root, info):
        return root.move_ids_without_package.move_line_nosuggest_ids