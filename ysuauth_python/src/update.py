import config
import apptime
import os
from git import Repo
from git.repo import Repo

import program_logs

if __name__ == "__main__":
    gitPath = os.environ.get("REPO_URL")
    gitBranch = os.environ.get("REPO_BRANCH")
    if gitPath is None or gitBranch is None:
        gitPath = 'https://gitee.com/a645162/ysuauth.git'
        gitBranch = 'develop'

    config.SaveConf("gitversion/date.ysuauth", apptime.getNow())
    savePath = os.getcwd() + "/gitversion/allfiles"
    program_logs.print1("将git仓库保存到" + savePath)

    if os.path.exists(savePath):
        program_logs.print1("脚本目录已经存在")
        os.rmdir(savePath)
    # r = Repo(savePath)
    Repo.clone_from(gitPath
                    , to_path=savePath, branch=gitBranch)
    program_logs.print1("更新脚本执行完毕！")
