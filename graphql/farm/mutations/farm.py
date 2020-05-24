from graphene import Mutation, Int, Boolean
from ..types.farm import Farm, InputFarm


class CreateFarm(Mutation):
    class Arguments:
        farm = InputFarm(required=True)

    Output = Farm

    @staticmethod
    def mutate(self, info, farm):

        if 'parcels' in farm:
            parcel_ids = []
            for parcel in farm['parcels']:
                parcel_ids.append((0, 0, parcel))
            farm['parcel_ids'] = parcel_ids
            farm.pop('parcels')

        env = info.context["env"]
        return env["agro.farm"].create(farm)


class RemoveFarm(Mutation):
    class Arguments:
        id = Int(required=True)

    removed = Boolean()

    @staticmethod
    def mutate(self, info, id):
        env = info.context["env"]
        return RemoveFarm(removed=env["agro.farm"].browse(id).unlink())