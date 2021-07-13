import time
import hmac
import hashlib
import base64
import urllib.parse

import datetime

import requests
import json
# https://developers.dingtalk.com/document/app/custom-robot-access

class DingTalk:

    def getToken(self, secret):
        timestamp = str(round(time.time() * 1000))
        # secret = 'this is secret'
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        # print(timestamp)
        # print(sign)
        return timestamp, sign

    def getAccessToken(self, url):
        return url[url.find("access_token=") + len("access_token="):]

    def getUrl(self, access_token, secret):
        if access_token.find("https://") != -1:
            access_token = self.getAccessToken(access_token)
        token = self.getToken(secret)
        return "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}" \
            .format(access_token, token[0], token[1])

    access_token = ""
    secret = ""
    url = ""

    def getFromFiles(self, path=""):
        with open(path + 'wh_access_token.dingtalk', 'r') as f:
            p = f.read().strip()
            if len(p) != 0:
                self.access_token = p

        with open(path + 'wh_secret.dingtalk', 'r') as f:
            p = f.read().strip()
            if len(p) != 0:
                self.secret = p

        self.url = self.getUrl(self.access_token,
                          self.secret)
        # print(self.access_token, self.secret)
        # print(self.url)

    nowtime = datetime.datetime.now()
    program = {
        "msgtype": "link",
        "link": {"text": "[{}] 联网成功！".format(datetime.datetime.strftime(nowtime, '%Y年%m月%d日 %H:%M:%S')),
                 "title": "联网成功",
                 "picUrl": "https://ysu.edu.cn/images/favicon.png",
                 "messageUrl": "http://auth.ysu.edu.cn"
                 },
        "at": {
            "isAtAll": True
        }
    }

    def sendMsg(self, msg):
        headers = {'Content-Type': 'application/json'}
        f = requests.post(self.url, data=json.dumps(msg), headers=headers)
        return f