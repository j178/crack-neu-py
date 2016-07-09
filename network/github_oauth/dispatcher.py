# Author: John Jiang
# Date  : 2016/7/7

# 如果写成这样的相对import, 当当前module执行的时候__name__永远为__main__，
# 无法根据__name__找到它在package中的位置，所以导入会出错
# from .config import configs
from network.github_oauth.config import configs

import cgi


def notfound(environ, start_response):
    # 第一个参数为HTTP状态值，第二个参数是一个列表，里面包含多个tuple,每个tuple代表一个回复头部
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    # 返回的必须是字节字符串
    return [b'Not Found']


class PathDispatcher:
    def __init__(self):
        self.pathmap = {}

    # 作为callback传给make_server,make_server负责将http请求解析好，传给这个回调
    # start_response是一个函数，调用它向请求回复response,有点像servlet,这两个参数都参不多
    def __call__(self, environ, start_response):
        # environ中包含了系统和HTTP请求的信息
        path = environ['PATH_INFO']
        # 从请求中提取查询参数，并放入一个类dict中,wsgi.input是一个file pointer
        params = cgi.FieldStorage(environ['wsgi.input'], environ=environ)

        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = {key: params.getvalue(key) for key in params}

        handler = self.pathmap.get((method, path), notfound)
        return handler(environ, start_response)

    def register(self, method, path, function):
        self.pathmap[method.lower(), path] = function
        return function
