#!/usr/bin/env python

"""
Convert a wikipedia article to a git repository and run gitk and git blame.

This is a much nicer way to find out where certain changes happened in a
wiki page.
"""

# Credits of the idea to https://gitlab.com/andreascian/mediawiki2git/

import time
import tempfile
from subprocess import run, Popen
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter as fmt

import mwclient


def main():
    args = get_args()
    revisions = mwclient.Site(args.site).Pages[args.article].revisions
    with tempfile.TemporaryDirectory() as tempdir:
        run(['git', 'init'], cwd=tempdir)
        for r in revisions(start=args.start, limit=args.limit, dir='newer',
                           prop='content|comment|user|timestamp'):
            commit(tempdir, r)

        Popen(['gitk'], cwd=tempdir)
        run(['git', 'blame', tempdir + '/article'], cwd=tempdir)
        input(f'\n\nPress enter to remove the temporal repository at {tempdir}')


def get_args():
    parser = ArgumentParser(description=__doc__, formatter_class=fmt)
    add = parser.add_argument
    add('article', help='name of the wikipedia article')
    add('--start', default='2019-01-01T00:00:00Z', help='oldest revision date')
    add('--limit', type=int, default=50, help='maximum number of revisions')
    add('--site', default='en.wikipedia.org', help='wikimedia site to access')
    return parser.parse_args()


def commit(dirname, revision):
    "Add revision as commit into a git-tracked directory at dirname"
    content = wrap(revision['*'])
    open(dirname + '/article', 'wt').write(content)
    run(['git', 'add', dirname + '/article'], cwd=dirname)
    run(['git', 'commit', '--message', revision.get('comment', '') or '<empty>',
         '--author', revision.get('user', '') + ' <no email>',
         '--date', time.asctime(revision['timestamp'])], cwd=dirname)


def wrap(text, maxsize=70):
    "Return text wrapped so lines have at most maxsize characteres"
    shorter_lines = []
    for line in text.splitlines():
        while len(line) > 70:
            i = (line.rfind(' ', 0, maxsize) + 1) or maxsize
            shorter_lines.append(line[:i])
            line = line[i:]
        shorter_lines.append(line)
    return '\n'.join(shorter_lines)



if __name__ == '__main__':
    main()
