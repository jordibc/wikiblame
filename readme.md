# Wikiblame

Convert a wikipedia article to a git repository and explore it with emacs in
version control mode (vs-annotate). Optionally run gitk and git blame too.

This is a much nicer way to find out where certain changes happened in a wiki
page.


```
usage: wikiblame.py [-h] [--start START] [--limit LIMIT] [--site SITE] [--gitk] [--git-blame] article

positional arguments:
  article        name of the wikipedia article

optional arguments:
  -h, --help     show this help message and exit
  --start START  oldest revision date (default: 2019-01-01T00:00:00Z)
  --limit LIMIT  maximum number of revisions (default: 50)
  --site SITE    wikimedia site to access (default: en.wikipedia.org)
  --gitk         see repository with gitk (default: False)
  --git-blame    see history with git blame (default: False)
```
