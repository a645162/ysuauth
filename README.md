# 燕山大学校园网验证脚本

YSU Auth

Only Simplified Chinese is supported
as this is an internal script of a Chinese school!

## 前言

本脚本核心的验证代码基于 YSU_netLogin 项目，占总项目的比例很小，
但是我还是选择开源整个项目，供大家学习，
作者现在已经毕业，要去别的学校读书了，应该是最后几次维护了，
希望有同学能接替我的工作，继续完善，在这里表示感谢。

本脚本参考
[BeingGod](https://github.com/BeingGod)
校友的
[YSU_netLogin](https://github.com/BeingGod/YSU_netLogin)
项目编写而成，
而 YSU_netLogin 项目好像是重写
[oPluss](https://github.com/OYCN)
的认证脚本。

在此对这两位表示感谢，故开源本脚本！

## 具体使用方法以及燕大校园网情况

我准备在 B站 上传一个视频

- 介绍校园网的情况
- 详细介绍校园网的使用
- 介绍这个脚本如何使用

视频的大纲请参考
[视频大纲](video/video.md)

## 版本说明

为了环境比较容易配置，以及容易设置开机自动启动，均发布至 Docker Hub，
当然，您可以可以自己编译 Docker 镜像。

### Docker Hub镜像
https://hub.docker.com/r/a645162/ysuauth

### ※DOCKER-COMPOSE(推荐)

除非不可以用docker-compose，否则请使用docker-compose！！！！

[示例文件](docker/docker-compose.yaml)

### 手动构建
可以在macOS或Linux下执行
mkimg.sh 脚本
，调用buildx构建
或者直接

```bash
docker build -f "Dockerfile_local" .
```

### Python版

由于大部分都是搬运自大佬，我只是修复bug，并且让他可以自动运行在我的树莓派。目前我没有太多要求。考研狗时间不够，我完研一定奥！一定完成！
Docker版还没有搞定~~我会抽时间搞定的！

### Kotlin版

https://github.com/YsKoala/YsuAuthCore

目前，Kotlin版本的核心代码我已经写好，但是今后应该没有机会将他变成Android应用了，
因此，如果您对此感兴趣，希望您能继续开发并将其发布出来！

## 联系我

你有什么问题要不就联系我QQ吧！备注清楚来意。

2018级 理学院 应用物理学 孔昊旻

QQ：846155976

E-Mail：a645162@qq.com

## 钉钉

[钉钉加群](https://h5.dingtalk.com/circle/healthCheckin.html?corpId=ding99dabd69bc14820726501c2c33ba7dcb)
也可以哦！

![dingding_qr_code](img/WechatIMG725.jpg)