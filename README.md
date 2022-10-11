# 燕山大学校园网验证脚本

## 前言

本脚本核心的验证代码基于YSU_netLogin项目，占总项目的比例很小，但是我还是选择开源整个项目，供大家学习，我现在大四了，有可能会放弃本项目，
也是希望有同学能接替我的工作，继续完成，在这里表示感谢。

<br>
本脚本参考 [BeingGod](https://github.com/BeingGod)
的 [YSU_netLogin](https://github.com/BeingGod/YSU_netLogin) 项目编写而成，
而YSU_netLogin项目好像是重写 [oPluss](https://github.com/OYCN) 校友的认证脚本
因此对这两位校友表示感谢，故开源本脚本

## 版本说明

为了环境比较容易配置，以及容易设置开机自动启动，我决定，今后的所有发版，均发布Docker容器，当然，您可以可以自己编译docker容器。

### Docker Hub镜像
https://hub.docker.com/r/a645162/ysuauth

### ※DOCKER-COMPOSE(推荐)

除非不可以用docker-compose，否则请使用docker-compose！！！！

```YAML
version: "3"
services:
  ysuauth_1: #第1个
    image: a645162/ysuauth:4.0.0
#    image: a645162/ysuauth:latest
    restart: always
    container_name: ysuauth
    deploy:
      resources:
        limits:
          cpus: '0.3'
          memory: 512M
        reservations:
          cpus: '0.2'
          memory: 200M
    network_mode: host
    tty: true
    volumes:
#      - /home/pi/ysuauth/settings:/ysuauth/settings
      - ./settings/:/ysuauth/settings/
#      - /home/pi/ysuauth/log:/ysuauth/log
      - ./logs/:/ysuauth/logs/
    environment:
    # 1、每个学生之间使用&隔开
    # 2、每个学生，请提供其对应密码
    # 3、请将大括号一并删除
    # 4、网络类型 0校园网 1中国移动 2中国联通 3中国电信
      - YSU_AUTH_USER="{201811080333} = {3}&{学号2} = {支持的网络类型}}" \
      - YSU_AUTH_USER_201811080333="{201811080333的密码}" \
      - YSU_AUTH_USER_{学号2}="{学号2的密码}" \
      - wh_access_token="{钉钉的Access Token}" \
      - wh_secret="{钉钉的Secret}" \
    # NIGHT_PAUSE用来控制是否夜间暂停工作，只有内容是1的时候才起作用
    # 本科生暑假不断电，但是断网
#      - NIGHT_PAUSE="1"

# 请将本文件的后戳名改为yml
```

### 手动构建
可以在macOS或Linux下执行mkimg.sh，调用buildx构建
或者直接docker build -f "Dockerfile_local" .

### Python版

由于大部分都是搬运自大佬，我只是修复bug，并且让他可以自动运行在我的树莓派。目前我没有太多要求。考研狗时间不够，我完研一定奥！一定完成！
Docker版还没有搞定~~我会抽时间搞定的！

### Kotlin版以及其他版本（本仓库中弃用）
目前，其他版本，我已经新建仓库。
<br>
我在我的大三上版学期遇到这个脚本，那时候仅仅完成了从Python到Kotlin的翻译，但是
本脚本从BeingGod的Python版本翻译到Kotlin目的是为了后面推出一个比较智能的Android App
<br>
Android App是否开源目前本人还在考虑当中

## 联系我
你有什么问题要不就联系我QQ吧！备注清楚来意，今年时间真的不够了，求求了~
<br><br>
2018级 理学院 应用物理学 孔昊旻
<br><br>
QQ：846155976
<br>
E-Mail：a645162@qq.com

## 钉钉
[钉钉加群](https://h5.dingtalk.com/circle/healthCheckin.html?corpId=ding99dabd69bc14820726501c2c33ba7dcb)
也可以哦！

![dingding_qr_code](img/WechatIMG725.jpg)