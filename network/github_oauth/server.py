# Author: John Jiang
# Date  : 2016/7/7
import hashlib
import time
import requests
from network.github_oauth.config import configs

access_token = None

_authorize_resp = '''\
<html>
  <head>
  </head>
  <body>
    <p>Well, hello there!</p>
    <p>We're going to now talk to the GitHub API. Ready?
      <a href="https://github.com/login/oauth/authorize?scope=user repo&client_id={client_id}">Click here</a> to
      begin!</a>
    </p>
    <p>
      If that link doesn't work, remember to provide your own <a href="/v3/oauth/#web-application-flow">Client ID</a>!
    </p>
  </body>
</html>'''

_localtime_resp = '''\
<?xml version="1.0"?>
<time>
  <year>{t.tm_year}</year>
  <month>{t.tm_mon}</month>
  <day>{t.tm_mday}</day>
  <hour>{t.tm_hour}</hour>
  <minute>{t.tm_min}</minute>
  <second>{t.tm_sec}</second>
</time>'''

_callback_resp = '''\
<html>
  <head>
  </head>
  <body>
    <p>Well, hello there!</p>
    <p>{}</p>
    <img src="{}" alt='Your avatar'>
  </body>
</html>'''


def authorize(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    # params = environ['params']
    resp = _authorize_resp.format(client_id=configs['client_id'])
    yield resp.encode('utf-8')


def localtime(environ, start_response):
    start_response('200 OK', [('Content-type', 'application/xml')])
    resp = _localtime_resp.format(t=time.localtime())
    yield resp.encode('utf-8')


# 这个页面有GitHub来访问，所以叫callback
def callback(environ, start_response):
    global access_token
    # 从GET参数中获取code
    # 用code换取access_token
    # 用access_token去请求信息
    code = environ['params'].get('code')
    # resp = _callback_resp.format(code=code)
    # start_response('200 OK', [('Content-Type', 'text/html')])
    # 如果不使用yield，就要返回一个list,里面包含一段一段的str
    # yield resp.encode('utf-8')
    url = 'https://github.com/login/oauth/access_token'
    data = {
        'client_id'    : configs['client_id'],
        'client_secret': configs['client_secret'],
        'code'         : code,
        'scope'        : 'user repo'
    }

    r = requests.post(url, data, headers={'Accept': 'application/json'})
    print(r.text)

    # 这个access_token没有时间限制，直到用户点击了revoke？还是说客户端自己做了储存？
    access_token = r.json()['access_token']
    r = requests.get('https://api.github.com/user', params={'access_token': access_token})
    info = r.json()
    resp = _callback_resp.format(info['email'], info['avatar_url'])
    start_response('200 OK', [('Content-Type', 'text/html')])
    yield resp.encode('utf-8')


# 微信公众号服务器验证
def wx_check_signature(environ, start_response):
    """
    开发者提交信息后，微信服务器将发送GET请求到填写的服务器地址URL上，GET请求携带四个参数：
    signature	微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数。
    timestamp	时间戳
    nonce	随机数
    echostr	随机字符串
    开发者通过检验signature对请求进行校验（下面有校验方式）。若确认此次GET请求来自微信服务器，请原样返回echostr参数内容，
    则接入生效，成为开发者成功，否则接入失败。

    加密/校验流程如下：
    1. 将token、timestamp、nonce三个参数进行字典序排序
    2. 将三个参数字符串拼接成一个字符串进行sha1加密
    3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信

    :param environ:
    :param start_response:
    :return:
    """
    signature = environ['params']['signature']
    timestamp = environ['params']['timestamp']
    nonce = environ['params']['nonce']
    echostr = environ['params']['echostr']
    token = 'test'
    params = [timestamp, nonce, token]
    params.sort()
    print(params)
    s = ''.join(params)

    if hashlib.sha1(s.encode()).hexdigest() == signature:
        start_response('200 OK', [('Content-Type', 'text/plain')])
        yield echostr.encode()


if __name__ == '__main__':
    from network.github_oauth.dispatcher import PathDispatcher
    from wsgiref.simple_server import make_server

    # Create the dispatcher and register functions
    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/authorize', authorize)
    dispatcher.register('GET', '/localtime', localtime)
    dispatcher.register('GET', '/callback', callback)
    dispatcher.register('GET', '/wx', wx_check_signature)

    # Launch a basic server
    httpd = make_server('', 80, dispatcher)
    print('Serving on port 80...')
    httpd.serve_forever()
