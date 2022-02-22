from python_framework import Enum, EnumItem


@Enum()
class UpdateMomentEnumeration :
    EIGHT_O_CLOCK = EnumItem(hour=8, minute=0)
    TWELVE_O_CLOCK = EnumItem(hour=12, minute=0)
    EIGHTEEN_O_CLOCK = EnumItem(hour=18, minute=0)
    TWENTY_THREE_THIRTY = EnumItem(hour=23, minute=30)

UpdateMoment = UpdateMomentEnumeration()
