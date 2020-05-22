from graphene import Mutation, String
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
        farm_created = env["agro.farm"].create(farm)

        return farm_created