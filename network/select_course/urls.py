# Author: John Jiang
# Date  : 2016/7/5

BASE_URL = 'http://202.118.31.243:8080/{}.XKAPPPROCESS'

# login - POST - 登陆
LOGIN_URL = BASE_URL.format('LOGIN_LOGININ')  # post

# user_info - GET - 用户能选课程的通用参数
COURSE_COMMON_INFO_URL = BASE_URL.format('XK_DISPLEFTFRAME')

# course_list - GET - 可选课程列表
COURSE_LIST_URL = BASE_URL.format('XK_QUERYCOURSE')

# task_info - GET - 教师列表
# 参数 CourseNO MajorLevel GradeYear MajorNO CourseModelID IfNeed
TASK_INFO_URL = BASE_URL.format('XK_GETTASKINFOBYCOURSE')

# task_turn - GET - 课程信息
# 参数 TaskID
TASK_TURN_URL = BASE_URL.format('XK_DISPTASKTURN')

# result - GET - 选课结果
RESULT_URL = BASE_URL.format('XK_DISPXKRESULT')

# select - GET - 选课
SELECT_URL = BASE_URL.format('XK_SELECTCOURSE')

# delete - GET - 删除已选课程
DELETE_URL = BASE_URL.format('XK_DELETECOURSE')

# exit - GET - 退出
EXIT_URL = BASE_URL.format('XK_EXITSELECT')

# stat - GET - 统计
STAT_URL = BASE_URL.format('XK_STATXKINFO')

# change pwd - GET - 修改密码
CHANGE_PWD_URL = BASE_URL.format('XK_DISPCHANGEUSERINFO')
