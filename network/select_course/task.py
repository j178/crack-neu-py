# Author: John Jiang
# Date  : 2016/7/6
from .base import Base
from .urls import *
import re


class Task(Base):
    def __init__(self, session, *data, **kwargs):
        self._task_id = None
        self._teacher = None
        self._description = None

        Base.__init__(self, session, *data, **kwargs)

    @property
    def task_id(self):
        """
        这样封装的意思是，未来task_id的实现可能会改变，而可以保持外部接口不变
        Java中必须写一大堆的getXX,setXX
        """
        return self._task_id

    @property
    def teacher(self):
        return self._teacher

    @property
    def description(self):
        return self._description

    def turn(self):
        """
        请求task的信息
        :return:
        """
        # todo
        html = self._session.get(TASK_TURN_URL, {'XKTaskID': self.task_id})
        text = html.text

    # todo 多线程抢课,错误处理
    def select(self):
        """
        选择课程
        """
        # 返回的是更新后的课表，填充在main frame中
        html = self._session.get(SELECT_URL, params={'XKTaskID': self.task_id})
        text = html.text

    def delete(self):
        """
        删除课程
        """
        html = self._session.get(DELETE_URL, params={'XKTaskID': self.task_id})
        text = html.text
