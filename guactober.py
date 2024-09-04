import json
import re
from github import Github

with open('.github_token') as gh_token_file:
    github_token = gh_token_file.read().strip()
    gh_token_file.close()

print("Getting list of Hacktoberfest repos from GitHub (be patient!)")
github_session = Github(github_token)
hacktoberfest_deps = []
hacktoberfest_repos = []
response = github_session.search_repositories(query=f'topic:hacktoberfest')
for repo in response:
    hacktoberfest_repos.append(repo.full_name)

with open('output.json') as guac_file:
    guac_data = json.load(guac_file)
    guac_file.close()

print("Searching your GUAC data")
for source_entry in guac_data['data']['HasSourceAt']:
    source = source_entry['source']['namespaces'][0]

    repo = source['namespace'] + '/' + source['names'][0]['name']

    if repo.startswith('github.com'):
        gh_name = re.sub('github.com/', '', repo)
        if gh_name in hacktoberfest_repos:
            hacktoberfest_deps.append(repo)
        
print("Here are the Hacktoberfest projects in your GUAC data:")
for dep in hacktoberfest_deps:
    print(dep)