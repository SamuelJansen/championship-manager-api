from python_framework import Controller, ControllerMethod, HttpStatus, EnumItemStr

from dto import AixSportsDto

@Controller(url = '/g1', tag='G1', description='G1 controller')
class G1Controller:

    @ControllerMethod(url='/',
        requestClass=[AixSportsDto.UpdateRequestDto],
        responseClass=[[dict]]
    )
    def put(self, dto):
        return self.service.g1WebScraper.update(dto), HttpStatus.OK

@Controller(url = '/g1', tag='G1', description='G1 controller')
class G1BatchController:

    @ControllerMethod(url='/all',
        responseClass=[[dict]]
    )
    def put(self):
        return self.service.g1WebScraper.updateAll(), HttpStatus.OK
