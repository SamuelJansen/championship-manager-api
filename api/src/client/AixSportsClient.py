from python_framework import HttpClient, HttpClientMethod

from config import AixSportsConfig, BrowserConfig


@HttpClient(
    url = AixSportsConfig.BASE_URL
)
class AixSportsClient :

    @HttpClientMethod(
        url = AixSportsConfig.CHAMPIONSHIP_URL,
        headers = {
          'authority': AixSportsConfig.AUTHORITY,
          'origin': AixSportsConfig.BASE_URL,
          'sec-fetch-dest': 'document',
          'sec-fetch-mode': 'navigate',
          'sec-fetch-user': '?1',
          'user-agent': BrowserConfig.USER_AGENT,
          'upgrade-insecure-requests': '1',
          'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-site': 'same-origin',
          'dnt': '1',
          'cookie': AixSportsConfig.SESSION_TOKEN
          # 'Content-Type': 'application/x-www-form-urlencoded'
        },
        consumes = 'application/x-www-form-urlencoded',
        produces = 'text/html; charset=UTF-8',
        # logRequest = True,
        # logResponse = True,
        returnOnlyBody = False,
        timeout = AixSportsConfig.CHAMPIONSHIP_TIMEOUT
        # , responseClass = [dict]
    )
    def updateChampionship(self, data, headers):
        return self.post(data=data, headers=headers)
