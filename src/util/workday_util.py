import datetime
import logging
from typing import Final

from domain.workday_dto import WorkdaySequence


class WorkdayUtils:
    """
    A static class for working with workdays
    """
    @staticmethod
    def create_workday_sequence(starting_day: datetime.date = None, ending_day: datetime.date = None):
        """
        starting_date: The date that we wish to start from
        ending_date: The date until we wish the data to be included

        Returns an instance of WorkdaySequence

        Raises ValueError if provided dates are incompatible
        """

        weekdays_names = []
        weekdays_dates = []
        delta_date = datetime.timedelta(1)

        if starting_day is None:
            logging.info('Did not pass a starting date. Using default values')
            starting_day = datetime.datetime.today()
        if ending_day is None:
            logging.info('Did not pass an ending date. Using default values')
            ending_day = (datetime.datetime.now() + datetime.timedelta(WorkdayConst.DEFAULT_DAYS_COUNT))

        current_day = starting_day

        try:
            while current_day <= ending_day:
                weekdays_names.append(current_day.strftime('%A'))
                weekdays_dates.append(current_day.strftime(WorkdayConst.DATE_FORMAT))
                current_day += delta_date
            return WorkdaySequence(weekdays_names, weekdays_dates)

        except Exception as e:
            logging.error(f'Error while calculating days: {e}')
            raise ValueError(f'Could not parse provided dates: {e}')


class WorkdayConst:
    DATE_FORMAT: Final[str] = '%d-%m-%Y'
    DEFAULT_DAYS_COUNT: Final[int] = 5
