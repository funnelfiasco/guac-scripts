# guactober

A script to search your GUAC data for projects partcipating in [Hacktoberfest](https://hacktoberfest.com).

## Requirements

* Python modules
    * json
    * re
    * PyGithub
* A GitHub token (either a PAT or classic token) in `./.github_token`

## Usage

After installing any missing requirements, run `python3 ./guactober.py`

The script assumes your query is in `./query.gql` and that your GraphQL query endpoint is `http://localhost:8080/query`.

The table below describes setting you may want to change.
All the settings described appear near the top of the script.

| Setting | Description
| ------- | -----------
| GITHUB_TOKEN_FILE | The path on disk to a file containing your GitHub token (and only your GitHub token)
| GRAPHQL_SERVER | The full URL to your GUAC GraphQL server's query endpoint


The script will print a list of repositories that are listed as participating in Hacktoberfest.

## License

This project is licensed under the [copyleft-next 0.3.1 license](LICENSE).

## Contributing

This is mostly a demo script, so I don't anticipate many contributions.
If you have them, I accept contributions under the [project's license](LICENSE).
By participating in this project, you agree to abide by the [Contributor Covenant](https://www.contributor-covenant.org/).
