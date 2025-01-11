#!/usr/bin/env python3

"""
Convert a wikipedia article to a git repository.

Then, offer to explore it with emacs in version control mode (vc-annotate),
or with git blame, or gitg.

This is a much nicer way to find out where certain changes happened in a
wiki page.
"""

# Credits of the idea go to https://gitlab.com/andreascian/mediawiki2git/

import sys
import time
import tempfile
from subprocess import run, Popen
from argparse import ArgumentParser, RawDescriptionHelpFormatter as fmt

try:
    import mwclient
except ModuleNotFoundError:
    sys.exit('Missing module mwclient.\n'
             'You can install it with: pip install mwclient')


def main():
    args = get_args()

    print(f'Getting revisions of "{args.article}" at {args.site} ...')

    page = mwclient.Site(args.site).Pages[args.article]

    revisions = []
    for rev in page.revisions(start=args.newest, end=args.oldest,
                              max_items=args.revisions,
                              prop='content|comment|user|timestamp'):
        if args.verbose:
            print('  %-24s  %-16s  %s' % (time.asctime(rev['timestamp']),
                                          rev.get('user', ''),
                                          rev.get('comment', '')[:50]))
        revisions.append(rev)

    with tempfile.TemporaryDirectory() as tempdir:
        # Init git repository.
        run(['git', 'init', '-b', 'main'], cwd=tempdir)

        # Add commits.
        for rev in reversed(revisions):  # from oldest to newest
            if '*' in rev:  # key "*" is for the contents of the article
                commit(rev, tempdir)
            else:
                print(f'\nSkipping revision without content: {dict(rev)}\n')

        # Examine the history.
        try:
            examine(tempdir)
        except FileNotFoundError as e:
            sys.exit(e)
        except (KeyboardInterrupt, EOFError):
            print()  # and the program ends


def get_args():
    parser = ArgumentParser(description=__doc__, formatter_class=fmt)
    add = parser.add_argument

    default_site = 'en.wikipedia.org'

    add('article', help='name of the wikipedia article')
    add('-n', '--revisions', metavar='N', type=int, help='number of revisions')
    add('--oldest', metavar='TIMESTAMP', help='oldest revision, like 2022-01-01T00:00:00Z')
    add('--newest', metavar='TIMESTAMP', help='newest revision (latest if not set)')
    add('--site', default=default_site, help=f'wikimedia site to access (default: {default_site})')
    add('-v', '--verbose', action='store_true', help='show retrieved revisions')

    args = parser.parse_args()

    if args.revisions is None and args.oldest is None:
        print('Using last 50 revisions. Use --revisions or --oldest otherwise.')
        args.revisions = 50

    return args


def commit(revision, dirname='/tmp'):
    "Add revision as a git commit in directory dirname"
    with open(dirname + '/article', 'wt') as f:
        text = wrap(revision['*'])
        f.write(text)

    run(['git', 'add', 'article'], cwd=dirname)

    run(['git', 'commit',
         '--quiet',
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

    options = ('  1. Open with emacs\n'
               '  2. Open with git blame\n'
               '  3. Open with gitg\n'
               '  4. Exit (it will remove %s)' % tempdir)

    print(options)

    while True:
        option = input('> ').strip()

        if option == '1':
            Popen(['emacs', '-eval', ('(progn'
                                      '  (find-file "article")'
                                      '  (vc-annotate "article" "HEAD")'
                                      '  (delete-other-windows))')],
                  cwd=tempdir)
        elif option == '2':
            run(['git', 'blame', 'article'], cwd=tempdir)
        elif option == '3':
            Popen(['gitg'], cwd=tempdir)
        elif option == '4':
            return
        elif option == '':
            pass
        else:
            print(f'Unknown option: {option}')
            print(f'Options:\n{options}')



if __name__ == '__main__':
    main()
