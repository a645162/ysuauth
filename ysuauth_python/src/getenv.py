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
        return wh_access_token, wh_secret


def getGitPath():
    gitPath = os.environ.get("REPO_URL")
    gitBranch = os.environ.get("REPO_BRANCH")

    if gitPath is None or gitBranch is None:
        gitPath = 'https://gitee.com/a645162/ysuauth.git'
        gitBranch = 'develop'

    return gitPath, gitBranch


def getEnv_isUseDefaultGit():
    use_git = os.environ.get("USE_DEFAULT_GIT")
    if use_git is None:
        return True
    else:
        use_git = str(use_git).strip()
        if use_git == "False":
            return False
        return True


def getSettingsPath():
    path = os.environ.get("SETTINGS_PATH")
    if path is None:
        return ""
    else:
        return path


def getLogsPath():
    path = os.environ.get("LOGS_PATH")
    if path is None:
        return ""
    else:
        return path


def getBasePath():
    path = os.environ.get("BASE_PATH")
    if path is None:
        return ""
    else:
        return path
