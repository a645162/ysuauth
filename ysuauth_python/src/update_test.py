import config
import apptime
import os
from git import Repo
from git.repo import Repo
import git
import shutil
import datetime

import program_logs

if __name__ == '__main__':
    repo = git.Repo("gitversion/allfiles")

    repo.remotes.origin.fetch()

    commits_behind = repo.iter_commits('develop..origin/develop')
    commits_ahead = repo.iter_commits('origin/develop..develop')
    count = sum(1 for c in commits_ahead)
    print(count)
