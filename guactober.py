import re
import os.path
from github import Github
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

###
#
# Things you might need to change
#
###

# Your GUAC GraphQL server
GRAPHQL_SERVER = "http://localhost:8080/query"

# File containing a PAT or classic token for GitHub authentication
# If this file does not exist, we'll use an unauthenticated session,
# which probably means you'll get rate limited.
GITHUB_TOKEN_FILE='.github_token'

###
#
# Things you probably won't need to change
#
###

# Test for a GitHub token file and setup the GitHub session
if os.path.exists(GITHUB_TOKEN_FILE):
    with open('.github_token') as gh_token_file:
        github_token = gh_token_file.read().strip()
        gh_token_file.close()
        github_session = Github(github_token)
else:
    github_session = Github()
    print("Using unauthenticated session for GitHub," + \
          "you may get rate limited!")

print("Getting list of Hacktoberfest repos from GitHub (be patient!)")
hacktoberfest_deps = []
hacktoberfest_repos = []
response = github_session.search_repositories(query=f'topic:hacktoberfest')
for repo in response:
    hacktoberfest_repos.append(repo.full_name)

print("Searching your GUAC data")
transport = AIOHTTPTransport(url=GRAPHQL_SERVER, headers=\
                    {'content-type': 'application/json'})
gql_client = Client(transport=transport)

with open('query.gql') as query_file:
    gql_query = query_file.read()
    query_file.close()

real_query = gql(gql_query)
guac_data = gql_client.execute(real_query)

for source_entry in guac_data['HasSourceAt']:
    source = source_entry['source']['namespaces'][0]

    repo = source['namespace'] + '/' + source['names'][0]['name']

    if repo.startswith('github.com'):
        gh_name = re.sub('github.com/', '', repo)
        if gh_name in hacktoberfest_repos:
            hacktoberfest_deps.append(repo)
        
print("Here are the Hacktoberfest projects in your GUAC data:")
for dep in hacktoberfest_deps:
    print(dep)