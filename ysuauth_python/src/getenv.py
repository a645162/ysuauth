import os


def is_docker():
    return os.environ.get("DOCKER") is not None


def is_git_mode():
    d = os.environ.get("USE_DEFAULT_GIT")
    if d is None:
        d = "False"

    return os.environ.get("DOCKER") \
           or os.path.exists("gitmode") \
           or os.path.exists("/ysuauth/gitmode") \
           or os.path.exists(getBasePath() + "/docker_status") \
           or d == "True"


def is_debug_mode():
    d = os.environ.get("DEBUG")
    if d is None:
        d = "False"

    return d.strip() == "True"


def get_user(key="YSU_AUTH_USER"):
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
        gitPath = 'https://gitee.com/yskoala/ysuauth.git'
        gitBranch = 'beta'

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
        return path.strip()


def getBasePath():
    path = os.environ.get("BASE_PATH")
    if path is None:
        return os.getcwd()
    else:
        create_dir_not_exist(path)
        return path


def create_dir_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)
