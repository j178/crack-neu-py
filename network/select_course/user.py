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
                status_forcelist=[400, 403, 404, 408, 500, 502]))


class User:
    def __init__(self, student_num, password):
        self._session = requests.session()
        self._session.mount('http://', ADAPTER_WITH_RETRY)

        self._num = student_num
        self._password = password
        self._name = None
        self._major = None
        self._grade = None
        self._class_ = None
        self._courses = []

    # todo 多线程同时抢滩登陆
    def login(self):
        """
        登录选课网站

        :return: 二元组，第一个表示登录是否成功，第二个表示失败的原因
        :rtype: tuple(bool,str)
        """
        data = {
            'strStudentNO': self._num,
            'strPassword' : self._password
        }

        r = self._session.post(LOGIN_URL, data)
        text = r.text
        # r.encoding = 'utf-8'
        pattern = r'id="StudentName" value="(?P<_name>.*?)".*?' \
                  r'id="StudentNO" readonly value="(?P<_num>.*?)".*?' \
                  r'id="MajorName" readonly value="(?P<_major>.*?)".*?' \
                  r'id="GradeName" readonly value="(?P<_grade>.*?)".*?' \
                  r'id="ClassName" readonly value="(?P<_class_>.*?)".*?'

        match = re.search(pattern, text, re.DOTALL)
        if match is not None:
            d = match.groupdict()
            # print(d)
            for key in d:
                setattr(self, key, d[key])
            return True, ''
        else:
            pattern = r'<font color="#FF0000" size="2"><strong>(.*?)</strong></font>'
            msg = re.search(pattern, text)

            return False, msg.group(1) if msg is not None else 'Unkonwn Error'

    def logout(self):
        self._session.get(EXIT_URL)

    def change_pwd(self, old, new):
        param = {
            'OldPassword'    : old,
            'NewPassword'    : new,
            'ConfirmPassowrd': new
        }
        # todo
        self._session.post(CHANGE_PWD_URL, param)

    def _course_init_attr(self):
        """
        获取当前用户默认的一些属性，在后面获取Task时使用
        """
        # todo 分类查找课程, 分页显示

        # 查询条件设置页，初始由服务器设置好了与账户匹配的信息，需要这里的信息和CourseID才能确定一个Task
        # 如果自定义了查询，后面请求Task的时候需要相应改变参数
        html = self._session.get(COURSE_COMMON_INFO_URL)
        text = html.text
        pattern = r'<select name="MajorLevel".*? value="(?P<major_level>\d+)" selected.*?</select>.*?' \
                  r'<input name="GradeYear" type="text" size="6" value="(?P<grade_year>.*?)">.*?' \
                  r'<select name="MajorNO".* <option value="(?P<major_num>.*?)" selected>.*?' \
                  r'<select name="IfNeed" .*?<option value="(?P<if_need>.*?)" selected>'

        r = re.search(pattern, text, re.DOTALL)
        if r is not None:
            Course.set_init_attr(r.groupdict())
        else:
            # retry
            pass

    def _get_courses(self, if_need='-1', course_kind4='-1', course_name='', course_mode_id=None):
        """
        根据查询条件获取可选课程

        :param str if_need: 课程的性质
            -1 全部性质
            1 公共基础课
            2 专业基础课
            3 全校性任选课
            4 专业任选课
            5 专业限选课
            6 人文选修课
            7 公共基础课(体育)
            8 暑期国际课
        :param course_kind4: 类别
            -1 全部类别
            1 必修课学分
            2 限选课学分
            3 外语毕业学分
            4 全校人文素质选修课
            5 暂不参与审核
            6 空任务
        :param str course_name: 课程名称
        :param course_mode_id: 默认不发送此参数
            1 必修
            2 限选
            3 任选
        :return: 返回Course对象的 Generator
        """

        if not Course.is_init_set():
            self._course_init_attr()
        if if_need != '-1':
            Course.if_need = if_need

        data = {
            'GradeYear'  : Course.grade_year,
            'MajorNO'    : Course.major_num,
            'IfNeed'     : if_need,
            'CourseKind1': '-1',
            'CourseKind2': '-1',
            'CourseKind3': '-1',
            'CourseKind4': course_kind4,
            'CourseName' : course_name,
            'WeekdayID'  : '',
            'Section'    : ''
        }
        # todo 缓存
        # 默认获取所有可选课程
        html = self._session.post(QUERY_COURSE_URL, data=data)
        text = html.text
        pattern = r'<tr id="ID\d+".*?QueryTaskInfo\(\'(?P<_course_num>.+?)\',\'\d+\',\'(?P<_course_model_id>\d+)\'.*?' \
                  r'title="(?P<_name>.+?)".*?' \
                  r'nowrap.*?>(?P<_type>.+?)</td>'

        for p in re.finditer(pattern, text, re.DOTALL):
            self._course.append(Course(self._session, p.groupdict()))

    @property
    def courses(self, if_need='-1', course_kind4='-1', course_name='', course_mode_id=None):
        # 第一次体会到了封装的真正含义，内部接口负责获取数据，外部接口决定如何向外部提供数据
        if not self._courses:
            self._get_courses(if_need, course_kind4, course_name, course_mode_id)
        return self._courses

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
