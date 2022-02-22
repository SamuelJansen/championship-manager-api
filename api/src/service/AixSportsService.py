from python_helper import log, ObjectHelper
from python_framework import Service, ServiceMethod

from config import AixSportsConfig as ASC
from dto import AixSportsDto


@Service()
class AixSportsService:

    @ServiceMethod(requestClass=[AixSportsDto.UpdateRequestDto])
    def update(self, dto):
        self.validator.aixSports.validateUpdateRequest(dto)
        return self.updateDataList(self.getDataList(dto.championshipIdList))


    @ServiceMethod()
    def updateAll(self):
        return self.updateDataList(self.getDataList([]))


    @ServiceMethod(requestClass=[[int]])
    def getDataList(self, championshipIdList):
        return self.service.g1WebScraper.getDataList(championshipIdList)


    @ServiceMethod(requestClass=[[int]])
    def getRequestDataList(self, championshipIdList):
        if ObjectHelper.isEmpty(championshipIdList):
            return self.repository.aixSports.findAllRequestData()
        return self.repository.aixSports.findAllRequestDataByChampionshipIdList(championshipIdList)


    def getRequestHeaders(self, aixSportsChampionshipId):
        return {
            ASC.REFERER_REQUEST_HEADER_KEY: ASC.CHAMPIONSHIP_DESTINY_URL.replace(
                ASC.CHAMPIONSHIP_ID_PLACEHOLDER,
                str(aixSportsChampionshipId)
            )
        }


    def getNewTeamRequest(self, rawData):
        rowIndex = rawData[ASC.RANK[ASC.REQUEST_BODY_KEY]] - 1
        return self.mapper.aixSports.fromRawDataToTeamRequest(rawData, rowIndex)


    def updateDataList(self, baseDataList):
        responseList = []
        for baseData in baseDataList:
            log.prettyPython(self.updateDataList, 'baseData', baseData, logLevel=log.DEBUG)
            g1ChampionshipData = baseData[ASC.CHAMPIONSHIP_DATA_KEY]
            aixSportsChampionshipId = baseData[ASC.REQUEST_DATA_KEY][ASC.CHAMPIONSHIP_ID_KEY]
            requestHeaders = self.getRequestHeaders(aixSportsChampionshipId)
            originUrl = baseData[ASC.REQUEST_DATA_KEY][ASC.ORIGIN_URL_KEY]
            destinyUrl = requestHeaders[ASC.REFERER_REQUEST_HEADER_KEY]
            requestData = baseData[ASC.REQUEST_DATA_KEY][ASC.REQUEST_BASE_DATA_KEY]
            for teamData in g1ChampionshipData:
                requestData = {
                    **requestData,
                    **self.getNewTeamRequest(teamData)
                }
            log.prettyPython(self.updateDataList, 'requestData', requestData, logLevel=log.DEBUG)
            responseBody, responseHeaders, responseStatus = self.client.aixSports.updateChampionship(
                headers = requestHeaders,
                data = requestData
            )
            responseList.append(self.mapper.aixSports.fromClientResponseToResponse(
                originUrl,
                destinyUrl,
                requestHeaders,
                requestData,
                responseStatus,
                responseBody
            ))
            log.prettyPython(self.updateDataList, 'responseData', responseList[-1], logLevel=log.DEBUG)
        log.prettyPython(self.updateDataList, 'responseData', responseList, logLevel=log.STATUS)
        return responseList
