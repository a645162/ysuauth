import getopt
import os
import shutil
import sys
import time

import git
# import GitPython
# from git import Repo
from git.repo import Repo

import apptime
import config
import getenv
import ping_simple
import program_logs


def commits_diff(repo, branch):
    commits_diff1 = repo.git.rev_list('--left-right', '--count', f'{branch}...{branch}@{{u}}')
    num_ahead, num_behind = commits_diff1.split('\t')
    program_logs.print1(f'num_commits_ahead: {num_ahead}')
    program_logs.print1(f'num_commits_behind: {num_behind}')
    return int(num_ahead), int(num_behind)


if __name__ == "__main__":
    argv = sys.argv[1:]
    needWait = False
    supportIgnore = False
    try:
        options, args = getopt.getopt(argv, "w", ["wait"])
    except getopt.GetoptError:
        sys.exit()

    for option, value in options:
        if option in ("-w", "--wait"):
            program_logs.print1("support wait connection!")
            needWait = True
        elif option in ("-i", "--ignoe"):
            program_logs.print1("support ignore connection!")
            supportIgnore = True

    if not supportIgnore:
        ping_value = 0

        if needWait:
            program_logs.print1("开始阻塞检测。")
        while True:
            ping_value = ping_simple.ping_host("gitee.com", 1)
            if not (needWait and ping_value == 0):
                break
            time.sleep(1)

        if ping_value == 0:
            exit(1)

        program_logs.print1("已经跳过了阻塞检测模块。")

    program_logs.print1("已经联网！")
    program_logs.print1("即将开始Update")

    base_path = getenv.getBasePath()
    git_dir = base_path + "/remote"
    getenv.create_dir_not_exist(git_dir)

    git_path = getenv.getGitPath()
    git_url = git_path[0]
    git_branch = git_path[1]

    config.SaveConf(git_dir + "/check_date.ysuauth", apptime.getNow())

    savePath = git_dir + "/allfiles"
    # getenv.create_dir_not_exist(savePath)
    program_logs.print1("将git仓库保存到" + savePath)

    isExist = os.path.exists(savePath)
    localLatestCommittime = 0
    if isExist and os.path.exists(git_dir + "/ready.ysuauth"):
        program_logs.print1("脚本目录已经存在")

        ok = False

        try:
            repo = git.Repo(savePath)
        except:
            program_logs.print1("原仓库存在问题！")
            program_logs.print1("重新clone！")
            shutil.rmtree(savePath)
            getenv.create_dir_not_exist(savePath)
            Repo.clone_from(git_url, to_path=savePath, branch=git_branch)
            repo = git.Repo(savePath)
            ok = True

        if not ok:
            os.chdir(git_dir)
            os.system('git remote update origin --prune')
            repo.remotes.origin.fetch()

            commits_diff = commits_diff(repo, git_branch)

            if commits_diff[0] > 0:
                program_logs.print1("???")
                program_logs.print1("这只能pull回来啊？！")
                program_logs.print1("pull回来的还能超前了？！")
                program_logs.print1("删了重新clone吧？！")
                shutil.rmtree(savePath)
                getenv.create_dir_not_exist(savePath)
                Repo.clone_from(git_url, to_path=savePath, branch=git_branch)
            elif commits_diff[1] == 0:
                program_logs.print1("git检查完毕！")
                program_logs.print1("当前版本为最新版本！")
            else:
                program_logs.print1("开始更新！")
                os.system("git pull")
    else:
        if isExist:
            shutil.rmtree(savePath)
        getenv.create_dir_not_exist(savePath)
        Repo.clone_from(git_url, to_path=savePath, branch=git_branch)

    config.SaveConf(git_dir + "/update_date.ysuauth", apptime.getNow())
    program_logs.print1("更新脚本执行完毕！")
    config.SaveConf(git_dir + "/ready.ysuauth", apptime.getNow())
