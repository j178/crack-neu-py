# Author: John Jiang
# Date  : 2016/7/6
from .base import Base
from .task import Task
from .urls import *
import re


class Course(Base):
    def __init__(self, session, *data, **kwargs):
        # todo super(Course,self).__init__与这个写法有什么区别？
        Base.__init__(self, session, *data, **kwargs)

    @property
    def tasks(self):
        self._common_attr.update({'CourseNO': self.id, 'CourseModelID': self.mode_id})
        # todo 缓存
        html = self._session.get(TASK_INFO_URL, params=self._common_attr)
        text = html.text

        pattern = r'<td nowrap.*?\'(?P<_task_id>.*?)\'.*?' \
                  r'<td align="center".*?>\s+(?P<_teacher>.*?)\s+</td>.*?' \
                  r'<span.*?>(?P<_description>.*?)&nbsp'

        for r in re.finditer(pattern, text, re.DOTALL):
            yield Task(self._session, r.groupdict())

    @property
    def id(self):
        return self._id

    @property
    def mode_id(self):
        return self._mode_id

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def common_attr(self):
        return self._common_attr

    # 没有定义这个连类的内部也无法创建属性吗？
    @common_attr.setter
    def common_attr(self, value):
        self._common_attr = value
