from python_helper import ObjectHelper, DateTimeHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus, EnumItem

from dto import AixSportsDto


@Validator()
class AixSportsValidator:

    @ValidatorMethod(requestClass=[AixSportsDto.UpdateRequestDto])
    def validateUpdateRequest(self, dto) :
        if ObjectHelper.isEmpty(dto.championshipIdList):
            raise GlobalException(message=f"Championship id list cannot be null nor empty: championshipIdList={dto.championshipIdList}", status=HttpStatus.BAD_REQUEST)
