# Gitlab CI Slack Fixer

We have a gitlab setup that hosts gitlab-ci and gitlab on the same host, under two different paths.
The gitlab-ci slack bot, however, fails to build the URL correctly.
This bot fixes that bot's mistake, reformatting the URLs.

## Usage

```ShellSession
$ python fixer.py $SLACK_TOKEN
```
