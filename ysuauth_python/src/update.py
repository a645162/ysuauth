import config
import apptime
import os
from git import Repo
from git.repo import Repo
import git
import shutil
import datetime

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

    isExist = os.path.exists(savePath)
    localLatestCommittime = 0
    if isExist:
        program_logs.print1("脚本目录已经存在")

        repo = git.Repo(savePath)
        tree = repo.tree()
        for blob in tree:
            commit = next(repo.iter_commits(paths=blob.path))
            blob_path = blob.path.strip()
            current_time = commit.committed_date
            print(blob_path, current_time,
                  datetime.datetime.fromtimestamp(current_time) \
                  .strftime("%Y年%m月%d日 %H:%M:%S"))
            if blob_path == "ysuauth_python":
                localLatestCommittime = current_time

        shutil.rmtree(savePath)
        # os.rmdir(savePath)
    print("代码最后一次提交时间为", localLatestCommittime)
    lastCommitTime = 0
    commitTimePath = "gitversion/commitdate.ysuauth"
    if os.path.exists(commitTimePath):
        with open(commitTimePath, "r") as f:
            t = f.read()
            try:
                t = int(t)
                lastCommitTime = t
            except Exception as e:
                lastCommitTime = 0
                raise e

    # r = Repo(savePath)
    Repo.clone_from(gitPath
                    , to_path=savePath, branch=gitBranch)
    program_logs.print1("更新脚本执行完毕！")
    program_logs.print1("准备执行重启脚本！")
    program_logs.execfile("restart.py")
    program_logs.print1("重启脚本执行完毕！")
