import git

import program_logs


def commits_diff(repo, branch):
    commits_diff = repo.git.rev_list('--left-right', '--count', f'{branch}...{branch}@{{u}}')
    num_ahead, num_behind = commits_diff.split('\t')
    # print(f'num_commits_ahead: {num_ahead}')
    # print(f'num_commits_behind: {num_behind}')
    return int(num_ahead), int(num_behind)


if __name__ == '__main__':
    repo = git.Repo("gitversion/allfiles")

    branch = "develop"
    repo.remotes.origin.fetch()

    # commits_diff = repo.git.rev_list('--left-right', '--count', f'{branch}...{branch}@{{u}}')
    # num_ahead, num_behind = commits_diff.split('\t')

    commits_diff = commits_diff(repo, branch)

    print(f'num_commits_ahead: {str(commits_diff[0])}')
    print(f'num_commits_behind: {commits_diff[1]}')

    if commits_diff[0] > 0:
        program_logs.print1("???")
        program_logs.print1("这只能pull回来啊？！")
        program_logs.print1("pull回来的还能超前了？！")
        program_logs.print1("删了重新clone吧？！")
