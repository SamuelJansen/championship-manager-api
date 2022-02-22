from python_helper import log
from python_framework import Mapper, MapperMethod, EnumItem, HttpStatus, FlaskUtil

import AixSportsConfig as ASC


@Mapper()
class AixSportsMapper:

    @MapperMethod(requestClass=[dict, int])
    def fromRawDataToTeamRequest(self, rawData, rowIndex) :
        log.prettyPython(self.fromRawDataToTeamRequest, 'rawData', rawData, logLevel=log.DEBUG)
        newTeamData = {
            f'class{self.getClassId(rowIndex)}[{ASC.ROW_ID[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.ROW_ID[ASC.REQUEST_BODY_KEY]],
            f'class{self.getClassId(rowIndex)}[{ASC.RANK[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.RANK[ASC.REQUEST_BODY_KEY]],
            f'class{self.getClassId(rowIndex)}[{ASC.TEAM_NAME[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.TEAM_NAME[ASC.REQUEST_BODY_KEY]],
            f'class{self.getClassId(rowIndex)}[{ASC.TEAM_POINT[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.TEAM_POINT[ASC.REQUEST_BODY_KEY]],
            f'class{self.getClassId(rowIndex)}[{ASC.TEAM_PLAYED_GAMES[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.TEAM_PLAYED_GAMES[ASC.REQUEST_BODY_KEY]],
            f'class{self.getClassId(rowIndex)}[{ASC.VICTORIES[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.VICTORIES[ASC.REQUEST_BODY_KEY]],
            f'class{self.getClassId(rowIndex)}[{ASC.DRAWS[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.DRAWS[ASC.REQUEST_BODY_KEY]],
            f'class{self.getClassId(rowIndex)}[{ASC.LOSSES[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.LOSSES[ASC.REQUEST_BODY_KEY]],
            f'class{self.getClassId(rowIndex)}[{ASC.UP_GOALS[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.UP_GOALS[ASC.REQUEST_BODY_KEY]],
            f'class{self.getClassId(rowIndex)}[{ASC.DOWN_GOALS[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.DOWN_GOALS[ASC.REQUEST_BODY_KEY]],
            f'class{self.getClassId(rowIndex)}[{ASC.NET_GOALS[ASC.REQUEST_BODY_KEY]}]': rawData[ASC.NET_GOALS[ASC.REQUEST_BODY_KEY]]
        }
        log.prettyPython(self.fromRawDataToTeamRequest, 'newTeamData', newTeamData, logLevel=log.DEBUG)
        return newTeamData


    @MapperMethod(requestClass=[str, str, dict, dict, EnumItem, str])
    def fromClientResponseToResponse(self, originUrl, destinyUrl, requestHeaders, requestData, responseStatus, responseBody) :
        return {
            'originUrl': originUrl,
            'destinyUrl': destinyUrl,
            'aixSportsRequestHeaders': requestHeaders,
            'aixSportsRequestData': requestData,
            'aixSportsResponseStatus': HttpStatus.map(responseStatus),
            'aixSportsResponseText': responseBody[FlaskUtil.CLIENT_RESPONSE_TEXT]
        }


    def getClassId(self, index):
        return f'{str(index):{"0"}>{3}}'
