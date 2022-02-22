import functools
from python_helper import log, ObjectHelper

from config import BrowserConfig
import G1Constants as G1C
import AixSportsConfig as ASC


G1_DATA_SHIFT = 1
MAX_ATEMPTS = 3


class G1WebScraper:

    def __init__(self, browserClient, hidden=BrowserConfig.HIDDEN):
        self.browserClient = browserClient
        self.hidden = hidden
        self.resetData()


    def resetData(self):
        self.dataHeaders = None
        self.rawData = None
        self.names = None


    def aggregadeData(self, dataList, key, data):
        for index, dataValue in enumerate(dataList):
            data[index][key] = dataValue


    def getDataHeaders(self):
        self.dataHeaders = self.dataHeaders if self.dataHeaders else [data.text for data in self.browserClient.findAllByClass('tabela__head--coluna', self.webPage)]
        log.prettyPython(self.getDataHeaders, 'dataHeaders', self.dataHeaders, logLevel=log.DEBUG)
        return self.dataHeaders


    def getRawData(self):
        self.rawData = self.rawData if self.rawData else [data.text for data in self.browserClient.findAllByClass('classificacao__pontos', self.webPage)]
        log.prettyPython(self.getRawData, 'rawData', self.rawData, logLevel=log.DEBUG)
        return self.rawData


    def getShiftedData(self, dataInfo, dataShift=0):
        self.dataHeaders = self.getDataHeaders()
        self.rawData = self.getRawData()
        self.names = self.getNames()
        teamQuantity = len(self.names)
        batchSize = len(self.rawData) // teamQuantity
        indexShift = -1
        for indexHeader, headerName in enumerate(self.dataHeaders):
            if headerName and dataInfo[G1C.DATA_HEADER_KEY] == headerName:
                indexShift = indexHeader - dataShift
                break
        shiftedData = [self.rawData[index * batchSize + indexShift] for index in range(teamQuantity)]
        log.prettyPython(self.getShiftedData, f'shiftedData - {dataInfo[G1C.DATA_HEADER_KEY]}', shiftedData, logLevel=log.DEBUG)
        return shiftedData


    def getNames(self):
        self.names = self.names if self.names else [data.text for data in self.browserClient.findAllByClass('classificacao__equipes classificacao__equipes--nome', self.webPage)]
        log.prettyPython(self.getNames, 'names', self.names, logLevel=log.DEBUG)
        return self.names


    def getPoints(self):
        points = [data.text for data in self.browserClient.findAllByClass('classificacao__pontos classificacao__pontos--ponto', self.webPage)]
        log.prettyPython(self.getPoints, 'points', points, logLevel=log.DEBUG)
        return points


    def assertValidCollection(self, collectionName, collection):
        assert ObjectHelper.isNotEmpty(collection), f'"{collectionName}" collection is empty: {collection}'
        assert functools.reduce(lambda x, y: x and y, [ObjectHelper.isNotEmpty(element) for element in collection]), f'"{collectionName}" collection contain only blank values: {collection}'


    def getChampionshipData(self, url, firstRowId, attempts=1):
        # example = [
        #     {
        #         'id': 0,
        #         'posicao': 0,
        #         'equipe': 'string',
        #         'pontos_ganhos': 'string',
        #         'jogos': 'string',
        #         'vitorias': 'string',
        #         'empates': 'string',
        #         'derrotas': 'string',
        #         'gols_pro': 'string',
        #         'gols_contra': 'string',
        #         'saldo_de_gols': 'string'
        #     }
        # ]
        try:
            log.status(self.getChampionshipData, f'Scraping data from "{url}". Attempt {MAX_ATEMPTS-attempts+1} from {MAX_ATEMPTS}')
            self.resetData()
            self.webPage = self.browserClient.accessUrl(url, self.browser)

            names = self.getNames()
            self.assertValidCollection('names', names)
            points = self.getPoints()
            self.assertValidCollection('points', points)
            playedGames = self.getShiftedData(G1C.TEAM_PLAYED_GAMES, dataShift=G1_DATA_SHIFT)
            self.assertValidCollection('playedGames', playedGames)

            victories = self.getShiftedData(G1C.VICTORIES, dataShift=G1_DATA_SHIFT)
            self.assertValidCollection('victories', victories)
            draws = self.getShiftedData(G1C.DRAWS, dataShift=G1_DATA_SHIFT)
            self.assertValidCollection('draws', draws)
            losses = self.getShiftedData(G1C.LOSSES, dataShift=G1_DATA_SHIFT)
            self.assertValidCollection('losses', losses)

            upGoals = self.getShiftedData(G1C.UP_GOALS, dataShift=G1_DATA_SHIFT)
            self.assertValidCollection('upGoals', upGoals)
            downGoals = self.getShiftedData(G1C.DOWN_GOALS, dataShift=G1_DATA_SHIFT)
            self.assertValidCollection('downGoals', downGoals)
            netGoals = self.getShiftedData(G1C.NET_GOALS, dataShift=G1_DATA_SHIFT)
            self.assertValidCollection('netGoals', netGoals)

            dataDictionary = {
                index: {
                    ASC.ROW_ID[ASC.REQUEST_BODY_KEY]: index + firstRowId,
                    ASC.RANK[ASC.REQUEST_BODY_KEY]: index + 1
                } for index in range(len(names))
            }
            self.aggregadeData(names, ASC.TEAM_NAME[ASC.REQUEST_BODY_KEY], dataDictionary)
            self.aggregadeData(points, ASC.TEAM_POINT[ASC.REQUEST_BODY_KEY], dataDictionary)
            self.aggregadeData(playedGames, ASC.TEAM_PLAYED_GAMES[ASC.REQUEST_BODY_KEY], dataDictionary)

            self.aggregadeData(victories, ASC.VICTORIES[ASC.REQUEST_BODY_KEY], dataDictionary)
            self.aggregadeData(draws, ASC.DRAWS[ASC.REQUEST_BODY_KEY], dataDictionary)
            self.aggregadeData(losses, ASC.LOSSES[ASC.REQUEST_BODY_KEY], dataDictionary)

            self.aggregadeData(upGoals, ASC.UP_GOALS[ASC.REQUEST_BODY_KEY], dataDictionary)
            self.aggregadeData(downGoals, ASC.DOWN_GOALS[ASC.REQUEST_BODY_KEY], dataDictionary)
            self.aggregadeData(netGoals, ASC.NET_GOALS[ASC.REQUEST_BODY_KEY], dataDictionary)
        except Exception as exception:
            log.failure(self.getChampionshipData, f'Not possible to get Championship data', exception=exception)
            if attempts > 1:
                return self.getChampionshipData(url, firstRowId, attempts=attempts-1)
            else:
                raise exception

        log.prettyPython(self.getChampionshipData, 'dataDictionary', dataDictionary, logLevel=log.DEBUG)
        self.resetData()
        return [*dataDictionary.values()]


    def getDataList(self, requestDataList):
        # example = {
        #     'request_data': {
        #         'aix_sports_championship_id': 0,
        #         'url': 'string',
        #         'first_row_id': 0,
        #         'request_base_data': {
        #             'nome': 'string',
        #             'template': 0,
        #             'fases0[id]': 0,
        #             'fases0[nome]': 'string',
        #             'grupos0[id]': 0,
        #             'grupos0[nome]': 'string'
        #         }
        #     },
        #     'data_dictionary': [
        #         {
        #             'id': 0,
        #             'posicao': 0,
        #             'equipe': 'string',
        #             'pontos_ganhos': 'string',
        #             'jogos': 'string',
        #             'vitorias': 'string',
        #             'empates': 'string',
        #             'derrotas': 'string',
        #             'gols_pro': 'string',
        #             'gols_contra': 'string',
        #             'saldo_de_gols': 'string'
        #         }
        #     ]
        # }
        self.browser = self.browserClient.getNewBrowser(hidden=self.hidden)
        try:
            dataList = [
                {
                    ASC.REQUEST_DATA_KEY: requestData,
                    ASC.CHAMPIONSHIP_DATA_KEY: self.getChampionshipData(requestData[ASC.ORIGIN_URL_KEY], requestData[ASC.FIRST_ROW_ID_KEY], attempts=MAX_ATEMPTS)
                } for requestData in requestDataList
            ]
            self.browserClient.close(self.browser)
        except Exception as exception:
            log.failure(self.getDataList, 'Not possible to get data list. Closing browser ', exception=exception)
            self.browserClient.close(self.browser)
            raise exception
        return dataList


    def getDataUnit(self, requestData):
        return self.getDataList([requestData])[0]
