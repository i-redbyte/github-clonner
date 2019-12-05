import json
import os

import git
import requests
from dotenv import load_dotenv
from git import GitCommandError, Remote, Repo
from requests.auth import HTTPBasicAuth
import links_from_header

load_dotenv()
token = os.getenv('TOKEN')
userName = os.getenv('USER_NAME')
organizationName = os.getenv('ORGANIZATION_NAME')
targetDir = os.getenv('TARGET_DIR')


def main_resp(url):
    return requests.get(url, auth=HTTPBasicAuth(userName, token))


def clone_or_rebase(repo_path, repo_name):
    try:
        repo = Repo(repo_path)
        if not repo.bare:
            origin = Remote(repo, 'origin')
            origin.pull(rebase=True)
            print('Repo at {} successfully pull --rebase.'.format(repo_path))

    except git.NoSuchPathError:
        try:
            git.Git(targetDir).clone(f'git@github.com:{repo_name}.git')
            print(f'Cloning {repos} success')
        except Exception:
            print(f'Fail on {repo_path}')


nextUrl = f"https://api.github.com/orgs/{organizationName}/repos?per_page=100"

while nextUrl:
    print(nextUrl)
    resp = main_resp(nextUrl)

    linkHeads = resp.headers.get('Link', None)
    if linkHeads:
        linkHeadsParsed = links_from_header.extract(linkHeads)
        nextUrl = linkHeadsParsed.get('next', None)
    else:
        nextUrl = None

    respCon = json.loads(resp.content)
    with open('repolist.txt', 'a') as fh:
        for rci in respCon:
            repos = rci["full_name"]
            print(f'!=Now=! {repos}')
            fh.writelines([f'{repos}\n'])
            path = f'{targetDir}/{repos.split("/")[1]}'
            clone_or_rebase(path, repos)
