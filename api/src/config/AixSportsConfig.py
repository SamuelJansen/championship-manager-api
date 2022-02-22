from python_helper import log
from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()


AUTHORITY = globalsInstance.getSetting('aix-sports.authority')
SESSION_TOKEN = globalsInstance.getSetting('aix-sports.session-token')
BASE_URL = globalsInstance.getSetting('aix-sports.base-url')
CHAMPIONSHIP_URL = globalsInstance.getSetting('aix-sports.championship.url')
CHAMPIONSHIP_TIMEOUT = globalsInstance.getSetting('aix-sports.championship.timeout')
CHAMPIONSHIP_ID_PLACEHOLDER = globalsInstance.getSetting('aix-sports.championship.id-placeholder')
CHAMPIONSHIP_DESTINY_URL = globalsInstance.getSetting('aix-sports.championship.destiny-url')
REFERER_REQUEST_HEADER_KEY = 'referer'


REQUEST_DATA_KEY = 'request_data'
CHAMPIONSHIP_DATA_KEY = 'championship_data'
REQUEST_BODY_KEY = 'request_body'

CHAMPIONSHIP_ID_KEY = 'championship_id'
ORIGIN_URL_KEY = 'origin_url'
FIRST_ROW_ID_KEY = 'first_row_id'
REQUEST_BASE_DATA_KEY = 'request_base_data'

ROW_ID = {
    REQUEST_BODY_KEY: 'id'
}
RANK = {
    REQUEST_BODY_KEY: 'posicao'
}
TEAM_NAME = {
    REQUEST_BODY_KEY: 'equipe'
}
TEAM_POINT = {
    REQUEST_BODY_KEY: 'pontos_ganhos'
}
TEAM_PLAYED_GAMES = {
    REQUEST_BODY_KEY: 'jogos'
}
VICTORIES = {
    REQUEST_BODY_KEY: 'vitorias'
}
DRAWS = {
    REQUEST_BODY_KEY: 'empates'
}
LOSSES = {
    REQUEST_BODY_KEY: 'derrotas'
}
UP_GOALS = {
    REQUEST_BODY_KEY: 'gols_pro'
}
DOWN_GOALS = {
    REQUEST_BODY_KEY: 'gols_contra'
}
NET_GOALS = {
    REQUEST_BODY_KEY: 'saldo_de_gols'
}
