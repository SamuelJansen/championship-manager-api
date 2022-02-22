from python_framework import Repository

from config import AixSportsConfig as ASC
from dummydata import ChampionshipDummyData


@Repository(model = dict)
class AixSportsRepository:

    def findAllRequestDataByChampionshipIdList(self, championshipIdList):
        return [{**data} for data in ChampionshipDummyData.REQUEST_DATA_LIST if data[ASC.CHAMPIONSHIP_ID_KEY] in championshipIdList]

    def findAllRequestData(self):
        return [{**data} for data in ChampionshipDummyData.REQUEST_DATA_LIST]
