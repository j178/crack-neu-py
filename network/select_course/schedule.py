# Author: John Jiang
# Date  : 2016/7/7
from .base import Base
import time


class Schedule(Base):
    def __init__(self, *data, **kwargs):
        self.weekday = None
        self.section = None
        self.span_of_weeks = None
        self.week_type = None
        self.teacher = None
        self.classroom = None
        self.building = None
        self.campus = None
        Base.__init__(self, *data, **kwargs)

    def __str__(self):
        return self.weekday + '|' + self.section + '|' + self.span_of_weeks + '|' + self.week_type + '|' \
               + self.teacher + '|' + self.classroom + '|' + self.building + '|' + self.campus
