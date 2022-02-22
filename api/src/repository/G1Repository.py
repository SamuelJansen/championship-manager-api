from python_framework import Repository

import ChampionshipDummyData


@Repository(model = dict)
class G1Repository:

    def getUrlDictionary(self):
        return {**ChampionshipDummyData.G1_URL_DICTIONARY}
