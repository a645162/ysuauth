import config
import apptime
import os
# import GitPython
from git import Repo
from git.repo import Repo
import git
import shutil
import datetime
import getenv

import program_logs


def commits_diff(repo, branch):
    commits_diff1 = repo.git.rev_list('--left-right', '--count', f'{branch}...{branch}@{{u}}')
    num_ahead, num_behind = commits_diff1.split('\t')
    program_logs.print1(f'num_commits_ahead: {num_ahead}')
    program_logs.print1(f'num_commits_behind: {num_behind}')
    return int(num_ahead), int(num_behind)


if __name__ == "__main__":
    base_path = getenv.getBasePath()
    git_dir = base_path + "/git"

    git_path = getenv.getGitPath()
    git_url = git_path[0]
    git_branch = git_path[1]

    config.SaveConf(git_dir + "/check_date.ysuauth", apptime.getNow())

    savePath = git_dir + "/allfiles"
    program_logs.print1("将git仓库保存到" + savePath)

    isExist = os.path.exists(savePath)
    localLatestCommittime = 0
    if isExist and os.path.exists(git_dir + "/ready.ysuauth"):
        program_logs.print1("脚本目录已经存在")

        repo = git.Repo(savePath)

        os.system('git remote update origin --prune')
        repo.remotes.origin.fetch()

        commits_diff = commits_diff(repo, git_branch)

        if commits_diff[0] > 0:
            program_logs.print1("???")
            program_logs.print1("这只能pull回来啊？！")
            program_logs.print1("pull回来的还能超前了？！")
            program_logs.print1("删了重新clone吧？！")
            shutil.rmtree(savePath)
            Repo.clone_from(git_path
                            , to_path=savePath, branch=git_branch)
        elif commits_diff[1] == 0:
            program_logs.print1("git检查完毕！")
            program_logs.print1("当前版本为最新版本！")
        else:
            program_logs.print1("开始更新！")
            os.system("git pull")
    elif isExist:
        shutil.rmtree(savePath)
        Repo.clone_from(git_path
                        , to_path=savePath, branch=git_branch)

    config.SaveConf(git_dir + "/update_date.ysuauth", apptime.getNow())
    program_logs.print1("更新脚本执行完毕！")
    config.SaveConf(git_dir + "/ready.ysuauth", apptime.getNow())
