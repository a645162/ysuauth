import urllib.parse
import urllib.request

import program_logs


# 封装post请求
def post(url, headers=None, data=None):
    program_logs.print1(str(data))
    if data is None:
        data = {}
    if headers is None:
        headers = {}
    program_logs.print1(urllib.parse.urlencode(data))
    response = None

    try:
        data = bytes(urllib.parse.urlencode(data), encoding='utf-8')
        request = urllib.request.Request(url, headers=headers, data=data)
        response = urllib.request.urlopen(request, timeout=20)
    except Exception as e:
        program_logs.print1(repr(e))
        raise e

    return response


# 封装get请求
def get(url, headers=None):
    if headers is None:
        headers = {}
    response = None
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request, timeout=10)

    except Exception as e:
        program_logs.print1(repr(e))
        raise e
    return response


def cleanup():
    urllib.request.urlcleanup()
