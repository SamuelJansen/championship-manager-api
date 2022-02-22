from python_framework import SchedulerType
from python_framework import Scheduler, SchedulerMethod, WeekDay, WeekDayConstant

from enumeration.UpdateMoment import UpdateMoment


@Scheduler()
class AixSportsScheduler :

    @SchedulerMethod(
        SchedulerType.CRON,
        week = WeekDayConstant.ALL_WEEK,
        weekDays = WeekDayConstant.WEEK_CHRON,
        hour = UpdateMoment.EIGHT_O_CLOCK.hour,
        minute = UpdateMoment.EIGHT_O_CLOCK.minute
    )
    def eightOClockUpdate(self) :
        self.service.aixSports.updateAll()


    @SchedulerMethod(
        SchedulerType.CRON,
        week = WeekDayConstant.ALL_WEEK,
        weekDays = WeekDayConstant.WEEK_CHRON,
        hour = UpdateMoment.TWELVE_O_CLOCK.hour,
        minute = UpdateMoment.TWELVE_O_CLOCK.minute
    )
    def twelveOClockUpdate(self) :
        self.service.aixSports.updateAll()


    @SchedulerMethod(
        SchedulerType.CRON,
        week = WeekDayConstant.ALL_WEEK,
        weekDays = WeekDayConstant.WEEK_CHRON,
        hour = UpdateMoment.EIGHTEEN_O_CLOCK.hour,
        minute = UpdateMoment.EIGHTEEN_O_CLOCK.minute
    )
    def eighteenOClockUpdate(self) :
        self.service.aixSports.updateAll()


    @SchedulerMethod(
        SchedulerType.CRON,
        week = WeekDayConstant.ALL_WEEK,
        weekDays = WeekDayConstant.WEEK_CHRON,
        hour = UpdateMoment.TWENTY_THREE_THIRTY.hour,
        minute = UpdateMoment.TWENTY_THREE_THIRTY.minute
    )
    def twentyThreeThirtyUpdate(self) :
        self.service.aixSports.updateAll()
