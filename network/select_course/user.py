# Author: John Jiang
# Date  : 2016/7/5
import re
import requests
import requests.adapters
from .urls import *
from .base import Base
from .course import Course

# auto retry
ADAPTER_WITH_RETRY = requests.adapters.HTTPAdapter(
        max_retries=requests.adapters.Retry(
                total=10,
                status_forcelist=[400, 403, 404, 408, 500, 502]
        )
)


class User:
    def __init__(self, student_num, password):
        self._session = requests.session()
        self._session.mount('http://', ADAPTER_WITH_RETRY)

        if student_num is not None and password is not None:
            self.login(student_num, password)

    def login(self, student_num, password):
        param = {
            'strStudentNO': student_num,
            'strPassword' : password
        }

        r = self._session.post(LOGIN_URL, param)
        # r.encoding = 'utf-8'
        pattern = r'id="StudentName" value="(?P<_name>.*?)".*?' \
                  r'id="StudentNO" readonly value="(?P<_num>.*?)".*?' \
                  r'id="MajorName" readonly value="(?P<_major>.*?)".*?' \
                  r'id="GradeName" readonly value="(?P<_grade>.*?)".*?' \
                  r'id="ClassName" readonly value="(?P<_class_>.*?)".*?'

        match = re.search(pattern, r.text, re.DOTALL)
        if match is not None:
            d = match.groupdict()
            # print(d)
            for key in d:
                setattr(self, key, d[key])
        else:
            # todo
            pass

    def logout(self):
        self._session.get(EXIT_URL)

    def change_pwd(self, old, new):
        param = {
            'OldPassword'    : old,
            'NewPassword'    : new,
            'ConfirmPassowrd': new
        }
        self._session.post(CHANGE_PWD_URL, param)

    @property
    def courses(self):
        html = self._session.get(COURSE_COMMON_INFO_URL)
        text = html.text
        # todo 缓存
        pattern = r'<select name="MajorLevel".*? value="(?P<MajorLevel>\d+)" selected.*?</select>.*?' \
                  r'<input name="GradeYear" type="text" size="6" value="(?P<GradeYear>.*?)">.*?' \
                  r'<select name="MajorNO".* <option value="(?P<MajorNO>.*?)" selected>.*?' \
                  r'<select name="IfNeed" .*?<option value="(?P<IfNeed>.*?)" selected>'
        r = re.search(pattern, text, re.DOTALL)

        if r is not None:
            course_common_info = r.groupdict()
        else:
            return

        # todo 缓存
        html = self._session.get(COURSE_LIST_URL)
        text = html.text
        pattern = r'<tr id="ID\d+".*?QueryTaskInfo\(\'(?P<_id>.+?)\',\'\d+\',\'(?P<_mode_id>\d+)\'.*?' \
                  r'title="(?P<_name>.+?)".*?' \
                  r'nowrap.*?>(?P<_type>.+?)</td>'

        for p in re.finditer(pattern, text, re.DOTALL):
            yield Course(self._session, p.groupdict(), _common_attr=course_common_info)

    @property
    def name(self):
        return self._name

    @property
    def num(self):
        return self._num

    @property
    def major(self):
        return self._major

    @property
    def grade(self):
        return self._grade

    @property
    def class_(self):
        return self._class_

    @property
    def result(self):
        html = self._session.get(RESULT_URL)
        return html.text

    @property
    def stat(self):
        html = self._session.get(STAT_URL)
        return html.text
