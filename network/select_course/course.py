# Author: John Jiang
# Date  : 2016/7/6
from .base import Base
from .task import Task
from .urls import *
import re


class Course(Base):
    # 一个用户不变的一些信息
    major_level = None
    grade_year = None
    major_num = None
    if_need = None
    # 上述默认属性是否设置
    _default_set = False

    def __init__(self, session, *data, **kwargs):
        self._name = None
        self._type = None
        self._course_num = None
        self._course_model_id = None
        Base.__init__(self, session, *data, **kwargs)

    @classmethod
    def set_init_attr(cls, data):
        """
        设置类的公共属性

        :param dict data: 公共信息
        """
        for key in data:
            setattr(cls, key, data[key])

        cls._default_set = True

    @classmethod
    def is_init_set(cls):
        """
        测试当前类的初始属性是否设置
        :return: bool
        """
        return cls._default_set

    @property
    def tasks(self):
        """
        获取课程对应的老师列表

        :return: generate Task对象
        :rtype generator of Task
        """
        params = {
            'CourseNO'     : self._course_num,
            'CourseModelID': self._course_model_id,
            'MajorLevel'   : Course.major_level,
            'GradeYear'    : Course.grade_year,
            'MajorNO'      : Course.major_num,
            'IfNeed'       : Course.if_need
        }

        # todo 缓存
        html = self._session.get(TASK_INFO_URL, params=params)
        text = html.text

        pattern = r'<td nowrap.*?\'(?P<_task_id>.*?)\'.*?' \
                  r'<td align="center".*?>\s+(?P<_teacher>.*?)\s+</td>.*?' \
                  r'<span.*?>(?P<_description>.*?)&nbsp'

        for r in re.finditer(pattern, text, re.DOTALL):
            yield Task(self._session, r.groupdict())

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type
