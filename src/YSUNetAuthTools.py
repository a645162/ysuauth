import json
import re

import req


class YSUNetAuth:
    def __init__(self):
        """
        登陆服务
        0：校园网
        1：中国移动
        2：中国联通
        3：中国电信
        """
        self.data = None
        self.services = {
            '0': '%e6%a0%a1%e5%9b%ad%e7%bd%91',
            '1': '%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8',
            '2': '%e4%b8%ad%e5%9b%bd%e8%81%94%e9%80%9a',
            '3': '%e4%b8%ad%e5%9b%bd%e7%94%b5%e4%bf%a1',
        }
        self.url = 'http://auth.ysu.edu.cn/eportal/InterFace.do?method='
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/85.0.4183.83 Safari/537.36',
            'Accept-Encoding': 'identify'
        }
        self.isLogin = None
        self.allData = None

    def tst_net(self, timeout=20):
        """
        测试网络是否认证
        :return: 是否已经认证
        """
        try:
            res = \
                req.get(
                    'http://auth.ysu.edu.cn',
                    headers=self.header,
                    timeout=timeout
                )
            # res = req.get('http://123.123.123.123', headers=self.header)
            # print(res.geturl())
            if res.geturl().find('success.jsp') > 0:
                self.isLogin = True
            else:
                self.isLogin = False
        except Exception as e:
            print(e.args)
            self.isLogin = False

        return self.isLogin

    def login(self, user, pwd, type):
        """
        输入参数登入校园网，自动检测当前网络是否认证。
        :param user:登入id
        :param pwd:登入密码
        :param type:认证服务
        :return:元祖第一项：是否认证状态；第二项：详细信息
        """

        # 注意喽：不用输入任何验证码，哪怕你 auth.ysu.edu.cn 提示你输入验证码了！

        if self.isLogin is None:
            self.tst_net()
        elif not self.isLogin:
            if user == '' or pwd == '':
                return False, '用户名或密码为空'

            try:
                res = req.get('http://auth.ysu.edu.cn', headers=self.header)
                r = res.read().decode('utf-8')
                queryString = re.findall(r"href='.*?\?(.*?)'", r, re.S)
                self.data = {'userId': user, 'password': pwd, 'service': self.services[type], 'operatorPwd': '',
                             'operatorUserId': '', 'validcode': "", 'passwordEncrypt': 'False',
                             'queryString': queryString[0]}

                res = req.post(self.url + 'login', headers=self.header, data=self.data)

                login_json = json.loads(res.read().decode('utf-8'))
                self.userindex = login_json['userIndex']
                # self.info = login_json
                self.info = login_json['message']
                if login_json['result'] == 'success':
                    return True, '认证成功'
                else:
                    return False, self.info
            except:
                return False, "Network Error!"
        return True, '已经在线'

    def get_allData(self):
        """
        获取当前认证账号全部信息
        #！！！注意！！！#此操作会获得账号alldata['userId']姓名alldata['userName']以及密码alldata['password']
        :return:全部数据的字典格式
        """
        res = req.get('http://auth.ysu.edu.cn/eportal/InterFace.do?method=getOnlineUserInfo', headers=self.header)
        try:
            self.allData = json.loads(res.read().decode('utf-8'))
        except json.decoder.JSONDecodeError as e:
            print('数据解析失败，请稍后重试。')
        alldata = self.allData
        print(self.allData)

        return self.allData

    def logout(self):
        """
        登出，操作内会自动获取特征码
        :return:元祖第一项：是否操作成功；第二项：详细信息
        """
        # if self.alldata == None:
        #     self.get_alldata()

        res = req.get(self.url + 'logout', headers=self.header)
        logout_json = json.loads(res.read().decode('utf-8'))
        # self.info = logout_json
        self.info = logout_json['message']
        if logout_json['result'] == 'success':
            return True, '下线成功'
        else:
            return False, self.info
