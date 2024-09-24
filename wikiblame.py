#!/usr/bin/env python3

"""
Convert a wikipedia article to a git repository.

Then, offer to explore it with emacs in version control mode (vc-annotate),
or with git blame, or gitg.

This is a much nicer way to find out where certain changes happened in a
wiki page.
"""

# Credits of the idea to https://gitlab.com/andreascian/mediawiki2git/

import sys
import time
import tempfile
from subprocess import run, Popen
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter as fmt

try:
    import mwclient
except ModuleNotFoundError:
    sys.exit('Missing module mwclient.\n'
             'You can install it with: pip install mwclient')


def main():
    args = get_args()

    revisions = mwclient.Site(args.site).Pages[args.article].revisions

    with tempfile.TemporaryDirectory() as tempdir:
        run(['git', 'init', '-b', 'main'], cwd=tempdir)

        print('Adding revisions...')
        for rev in revisions(start=args.start, end=args.end, dir='newer',
                             #max_items=args.max_items,  # TODO: use correctly
                             prop='content|comment|user|timestamp'):
            if '*' in rev:  # key "*" is for the contents of the article
                commit(rev, tempdir, args.verbose)
            else:
                print(f'\nSkipping revision without content: {dict(rev)}\n')

        try:
            examine(tempdir)
        except FileNotFoundError as e:
            sys.exit(e)
        except (KeyboardInterrupt, EOFError):
            print()  # and the program ends


def get_args():
    parser = ArgumentParser(description=__doc__, formatter_class=fmt)
    add = parser.add_argument

    add('article', help='name of the wikipedia article')
    add('--start', default='2022-01-01T00:00:00Z', help='oldest revision date')
    add('--end', help='newest revision date (latest revision if not set)')
#    add('--max-items', type=int, help='maximum number of revisions') # TODO
    add('--site', default='en.wikipedia.org', help='wikimedia site to access')
    add('-v', '--verbose', action='store_true', help='show commit messages')

    return parser.parse_args()


def commit(revision, dirname='/tmp', verbose=False):
    "Add revision as a git commit in directory dirname"
    with open(dirname + '/article', 'wt') as f:
        f.write(wrap(revision['*']))

    run(['git', 'add', 'article'], cwd=dirname)

    run(['git', 'commit',
         '--no-quiet' if verbose else '--quiet',
         '--no-verify',  # in case the user has pre-commit or commit-msg hooks
         '--message', revision.get('comment', '') or '<empty>',
         '--author', revision.get('user', '') + ' <no email>',
         '--date', time.asctime(revision['timestamp'])],
        cwd=dirname)


def wrap(text, maxsize=70):
    "Return text wrapped so lines have at most maxsize characters"
    shorter_lines = []

    for line in text.splitlines():
        while len(line) > maxsize:  # keep breaking the line
            i = (line.rfind(' ', 0, maxsize) + 1) or maxsize
            shorter_lines.append(line[:i])
            line = line[i:]

        shorter_lines.append(line)  # append the last bit

    return '\n'.join(shorter_lines)


def examine(tempdir):
    "Ask and examine the revision history for the article in tempdir"
    print('\nDirectory with the history as a git repository:', tempdir)

    while True:
        print('1. Open with emacs')
        print('2. Open with git blame')
        print('3. Open with gitg')
        print('4. Exit (it will remove %s)' % tempdir)

        answer = input('> ').strip()

        if answer == '1':
            Popen(['emacs', '-eval', ('(progn'
                                      '  (find-file "article")'
                                      '  (vc-annotate "article" "HEAD")'
                                      '  (delete-other-windows))')],
                  cwd=tempdir)
        elif answer == '2':
            run(['git', 'blame', 'article'], cwd=tempdir)
        elif answer == '3':
            Popen(['gitg'], cwd=tempdir)
        elif answer == '4':
            return



if __name__ == '__main__':
    main()
