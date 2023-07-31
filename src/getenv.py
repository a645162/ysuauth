import os

import apptime


def is_docker():
    return os.environ.get("DOCKER") is not None


def is_git_mode():
    d = os.environ.get("USE_DEFAULT_GIT")
    if d is None:
        d = "False"

    return (
            os.environ.get("DOCKER")
            or os.path.exists("git_mode")
            or os.path.exists("git_mode.ysuauth")
            or os.path.exists("/ysuauth/git_mode")
            or os.path.exists("/ysuauth/git_mode.ysuauth")
            or os.path.exists(getBasePath() + "/docker_status")
            or d == "True"
    )


def is_debug_mode():
    d = os.environ.get("DEBUG")
    if d is None:
        d = "False"

    return d.strip() == "True"


def is_ignore_work_time():
    d = os.environ.get("IGNORE_WORK_TIME")
    if d is None:
        d = "False"

    return d.strip() == "True"


def get_night_pause():
    np = os.environ.get("NIGHT_PAUSE")
    if np is None:
        return False
    env_np = str(np).strip()
    return env_np == "1"


def get_user():
    key = "YSU_AUTH_USER"
    return os.environ.get(key)


def getPwd(stu_id):
    return os.environ.get("YSU_AUTH_USER_" + str(stu_id))


def split_time_str(time_str):
    time_str_l = str(time_str).split(":")
    if len(time_str_l) == 2:
        try:
            t1 = int(time_str_l[0])
            t2 = int(time_str_l[1])
            return t1, t2
        except:
            return None
    else:
        return None


def isDingTalkEnable():
    DingTalk_Enable = os.environ.get("DingTalk_Enable")

    if DingTalk_Enable is not None and str(DingTalk_Enable).strip() == "1":

        DingTalkWork_Time_Start = os.environ.get("DingTalkWork_Time_Start").strip()
        DingTalkWork_Time_End = os.environ.get("DingTalkWork_Time_End").strip()

        time_start = split_time_str(DingTalkWork_Time_Start)
        time_end = split_time_str(DingTalkWork_Time_End)

        if time_start is None or time_end is None:
            return False
        else:
            return apptime.isInTime(time_start, time_end)
    else:
        return False


def getDingTalk():
    wh_access_token = os.environ.get("wh_access_token")
    wh_secret = os.environ.get("wh_secret")
    if wh_secret is None or wh_access_token is None:
        return None
    else:
        return wh_access_token, wh_secret


def time_str_2_time():
    pass


def getUserTimes():
    Logout_Time_Start = os.environ.get("Logout_Time_Start").strip()
    Logout_Time_End = os.environ.get("Logout_Time_End").strip()

    logout_time1 = split_time_str(Logout_Time_Start)
    logout_time2 = split_time_str(Logout_Time_End)

    if logout_time1 is None or logout_time2 is None:
        logout_time = None
    else:
        logout_time = logout_time1, logout_time2

    StartWork_Time_Start = os.environ.get("StartWork_Time_Start").strip()
    StartWork_Time_End = os.environ.get("StartWork_Time_End").strip()

    start_time1 = split_time_str(StartWork_Time_Start)
    start_time2 = split_time_str(StartWork_Time_End)

    if start_time1 is None or start_time2 is None:
        start_time = None
    else:
        start_time = start_time1, start_time2

    return start_time, logout_time


def getGitPath():
    gitPath = os.environ.get("REPO_URL")
    gitBranch = os.environ.get("REPO_BRANCH")

    if gitPath is None or gitBranch is None:
        gitPath = "https://gitee.com/a645162/ysuauth.git"
        gitBranch = "master"

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
