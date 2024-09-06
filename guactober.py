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

def queryGithub():
    '''
    Search for GitHub repos with the "hacktoberfest" topic

    Inputs: none
    Outputs: gh_participants (list)
    '''
    gh_participants = []
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

    response = github_session.search_repositories(query=f'topic:hacktoberfest')
    for repo in response:
        gh_participants.append(repo.full_name)

    return gh_participants

def queryGuac():
    '''
    Search the data in GUAC and return anything with HasSrcAt

    Inputs: none
    Outputs: sources (list)
    '''
    sources = []
    print("Searching your GUAC data")
    transport = AIOHTTPTransport(url=GRAPHQL_SERVER, headers=\
                    {'content-type': 'application/json'})
    gql_client = Client(transport=transport)

    with open('query.gql') as query_file:
        gql_query = gql(query_file.read())
        query_file.close()

    guac_data = gql_client.execute(gql_query)

    for source_entry in guac_data['HasSourceAt']:
        source = source_entry['source']['namespaces'][0]
        sources.append(source['namespace'] + '/' + source['names'][0]['name'])

    return sources

def findProjects(sources, participants):
    '''
    Search the participants from GitHub and GitLab in our GUAC data

    Inputs: sources (list), participants(list)
    Outputs: none
    '''
    hacktoberfest_deps = []
    for repo in sources:
        if repo.startswith('github.com') or repo.startswith('gitlab.com'):
            name = re.sub('git(hub|lab).com/', '', repo)
            if name in participants:
                hacktoberfest_deps.append(repo)

    print("Here are the Hacktoberfest projects in your GUAC data:")
    for dep in hacktoberfest_deps:
        print(dep)

sources = queryGuac()

# Search the forges for participating projects
participants = []
participants.extend(queryGithub())

findProjects(sources, participants)
