#!/usr/bin/env python

"""
Convert a wikipedia article to a git repository and explore it with emacs in
version control mode (vc-annotate). Optionally run gitk and git blame too.

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
        run(['git', 'init', '-b', 'master'], cwd=tempdir)
        for rev in revisions(start=args.start, limit=args.limit, dir='newer',
                             prop='content|comment|user|timestamp'):
            if '*' in rev:  # key "*" is for the contents of the article
                commit(rev, tempdir)
            else:
                print(f'\nSkipping revision without content: {dict(rev)}\n')

        Popen(launch_emacs_with_git_blame, cwd=tempdir)

        if args.gitk:
            Popen(['gitk'], cwd=tempdir)

        if args.git_blame:
            run(['git', 'blame', 'article'], cwd=tempdir)

        print(f'\nDirectory with the history as a git repository: {tempdir}')
        input(f'Press enter to remove the temporal directory... ')  # pauses


def get_args():
    parser = ArgumentParser(description=__doc__, formatter_class=fmt)
    add = parser.add_argument
    add('article', help='name of the wikipedia article')
    add('--start', default='2019-01-01T00:00:00Z', help='oldest revision date')
    add('--limit', type=int, default=50, help='maximum number of revisions')
    add('--site', default='en.wikipedia.org', help='wikimedia site to access')
    add('--gitk', action='store_true', help='see repository with gitk')
    add('--git-blame', action='store_true', help='see history with git blame')
    return parser.parse_args()


def commit(revision, dirname='/tmp'):
    "Add revision as a git commit in directory dirname"
    open(dirname + '/article', 'wt').write(wrap(revision['*']))
    run(['git', 'add', 'article'], cwd=dirname)
    run(['git', 'commit', '--message', revision.get('comment', '') or '<empty>',
         '--author', revision.get('user', '') + ' <no email>',
         '--date', time.asctime(revision['timestamp'])], cwd=dirname)


def wrap(text, maxsize=70):
    "Return text wrapped so lines have at most maxsize characters"
    shorter_lines = []
    for line in text.splitlines():
        while len(line) > maxsize:
            i = (line.rfind(' ', 0, maxsize) + 1) or maxsize
            shorter_lines.append(line[:i])
            line = line[i:]
        shorter_lines.append(line)
    return '\n'.join(shorter_lines)


launch_emacs_with_git_blame = [
    'emacs', '-eval',
        '(progn'
        '  (find-file "article")'
        '  (vc-annotate "article" "HEAD")'
        '  (delete-other-windows))']



if __name__ == '__main__':
    main()
