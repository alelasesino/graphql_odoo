from graphene import ObjectType, String, Int


class Product(ObjectType):
    id = Int()
    display_name = String()
    code = String()
    barcode = String()
    categ_id = Int()
    image = String()

    @staticmethod
    def resolve_image(root, info):
        return root.image_512