import os


def getUser(key="YSU_AUTH_USER"):
    return os.environ.get(key)


def getPwd(stu_id):
    return os.environ.get("YSU_AUTH_USER_" + str(stu_id))


def getDingTalk():
    wh_access_token = os.environ.get("wh_access_token")
    wh_secret = os.environ.get("wh_secret")
    if wh_secret is None or wh_access_token is None:
        return None
    else:
        return (wh_access_token, wh_secret)


def getGit():
    use_git = os.environ.get("USE_GIT")
    if use_git is None:
        return False
    else:
        return True
