# Author: John Jiang
# Date  : 2016/7/6
from network.select_course.user import User

if __name__ == '__main__':
    u = User('20144633', '2025642313')
    for c in u.courses:
        # print(c.id, c.name, c.type)
        for t in c.tasks:
            print(c.name, t.task_id, t.teacher, t.description)
