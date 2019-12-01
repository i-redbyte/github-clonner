import json
import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import links_from_header

load_dotenv()
token = os.getenv('TOKEN')
userName = os.getenv('USER_NAME')
organizationName = os.getenv('ORGANIZATION_NAME')


def main_resp(url):
    return requests.get(url, auth=HTTPBasicAuth(userName, token))


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
        fh.writelines([f'{respconi["full_name"]}\n' for respconi in respCon])
