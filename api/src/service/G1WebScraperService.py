from python_helper import ObjectHelper
from python_framework import Service, ServiceMethod, EnumItem

from config import AixSportsConfig as ASC
from dto import AixSportsDto

from service.webscraper.G1WebScraper import G1WebScraper


@Service()
class G1WebScraperService :

    @ServiceMethod(requestClass=[[int]])
    def getDataList(self, championshipIdList):
        requestDataList = self.getRequestDataList(championshipIdList)
        if ObjectHelper.isEmpty(requestDataList):
            return []
        return G1WebScraper(self.client.browser).getDataList(requestDataList)


    @ServiceMethod(requestClass=[AixSportsDto.UpdateRequestDto])
    def update(self, dto):
        self.validator.aixSports.validateUpdateRequest(dto)
        return self.service.aixSports.updateDataList(self.getDataList(dto.championshipIdList))


    @ServiceMethod()
    def updateAll(self):
        return self.service.aixSports.updateDataList(self.getDataList([]))


    @ServiceMethod(requestClass=[[int]])
    def getRequestDataList(self, championshipIdList):
        return [
            {
                **aixSportsRequestData,
                **{
                    ASC.ORIGIN_URL_KEY: self.getUrlDictionary()[aixSportsRequestData[ASC.CHAMPIONSHIP_ID_KEY]]
                }
            } for aixSportsRequestData in self.service.aixSports.getRequestDataList(championshipIdList)
        ]


    def getUrlDictionary(self):
        return self.repository.g1.getUrlDictionary()


    def getAixSportsChampionshipId(self, data):
        return data[ASC.REQUEST_DATA_KEY][ASC.CHAMPIONSHIP_ID_KEY]
