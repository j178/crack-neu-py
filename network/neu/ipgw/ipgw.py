# Author: John Jiang
# Date  : 2016/7/1

# 开机自动登陆，关机自动退出脚本
# todo 通过「校园统一身份认证SSO」修改任何人的校园网密码

import requests
import re
import pickle
import sys

page_url = 'http://ipgw.neu.edu.cn:802/srun_portal_pc.php'
ajax_url = 'http://ipgw.neu.edu.cn:802/include/auth_action.php'


def save_cookies(requestCookieJar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests.utils.dict_from_cookiejar(requestCookieJar), f)


def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def login(username, password):
    """
    登陆IP网关并获取网络使用情况

    :param str username: 学号
    :param str password: 密码
    """
    data = {
        'action'  : 'login',
        'username': username,
        'password': password,
    }

    # 不需要cookie，服务器根据；请求的IP来获取登录的用户的信息
    # s = requests.session()
    r = requests.post(page_url, data)

    # save_cookies(r.cookies, 'cookie')

    if re.search('网络已连接', r.text):
        print('网络已连接')

        # 如果未登录，则返回not_online
        r = requests.post(ajax_url, data={'action': 'get_online_info'})
        info = r.text.split(',')
        print('用户名: ', username)
        print('已用流量: {:.2f} GB'.format(float(info[0]) / 1e9))
        print('已用时长: {:.2f} h'.format(float(info[1]) / 3600))
        print('帐户余额:', info[2])
        print('IP地址:', info[5])
        return True
    else:
        msg = re.search(r'<input.*?name="url".*?<p>(.*?)</p>', r.text, re.DOTALL)
        if msg:
            print(msg.group(1))
        return False


def logout(username):
    """
    登出IP网关

    :param str username:
    """
    data = {
        'action'  : 'logout',
        'username': username,
        'password': '',
        'ajax'    : '1'
    }

    r = requests.post(ajax_url, data)
    r.encoding = 'utf-8'
    print(r.text)


if __name__ == '__main__':

    if sys.argv[1] == '-i':
        login(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == '-o':
        logout(sys.argv[2])
