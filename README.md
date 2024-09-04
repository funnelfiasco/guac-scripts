# guactober

A script to search your GUAC data for projects partcipating in [Hacktoberfest](https://hacktoberfest.com).

## Requirements

* Python modules
    * json
    * re
    * PyGithub
* A GitHub token (either a PAT or classic token) in `./.github_token`

## Usage

First, get the data you need from your GUAC instance's GraphQL playground:

1. Paste TODO
2. Run the TODO
3. Copy the output to `./output.json`

Then run this script:

1. `python3 ./guactober.py`

The script will print a list of repositories that are listed as participating in Hacktoberfest.

## License

This project is licensed under the [GNU General Public License version 3](LICENSE).

## Contributing

This is mostly a demo script, so I don't anticipate many contributions.
If you have them, I accept contributions under the [project's license](LICENSE).
By participating in this project, you agree to abide by the [Contributor Covenant](https://www.contributor-covenant.org/).
