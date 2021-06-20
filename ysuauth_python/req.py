import urllib.request
import urllib.parse


# 封装post请求
def post(url, headers={}, data={}):
    # print(str(data))
    print(urllib.parse.urlencode(data))
    data = bytes(urllib.parse.urlencode(data), encoding='utf-8')
    request = urllib.request.Request(url, headers=headers, data=data)
    response = urllib.request.urlopen(request, timeout=20)
    return response


# 封装get请求
def get(url, headers={}):
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request, timeout=10)
    return response
