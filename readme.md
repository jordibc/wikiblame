# Wikiblame

Convert a wikipedia article to a git repository.

Then, offer to explore it with emacs in version control mode
(vc-annotate), or with git blame, or gitg.

This is a much nicer way to find out where certain changes happened in
a wiki page.


## 📥 Installation

You can run the `wikiblame.py` file directly, or install the
executable `wikiblame` with:

```sh
pip install -e .
```


## 🔋 Dependencies

Wikiblame uses the [mwclient](https://github.com/mwclient/mwclient)
module to communicate with the MediaWiki API.

It is packaged in most systems (for example, as `python3-mwclient` in
Debian), but you can also install it with:

```sh
pip install mwclient
```

It also uses [git](https://git-scm.com/) to create a local repository
with one commit per revision of the article.

Depending on the program you want to use to see the history of the
file, you may want to have emacs and/or gitg too.


## 📖 Usage

```
usage: wikiblame [-h] [-n N] [--oldest TIMESTAMP] [--newest TIMESTAMP] [--site SITE] [-v] article

positional arguments:
  article        name of the wikipedia article

options:
  -h, --help           show this help message and exit
  -n N, --revisions N  number of revisions
  --oldest TIMESTAMP   oldest revision, like 2022-01-01T00:00:00Z
  --newest TIMESTAMP   newest revision (latest if not set)
  --site SITE          wikimedia site to access (default: en.wikipedia.org)
  -v, --verbose        show retrieved revisions
```


## 💡 Examples

### Simple use

In this example we see the history of the article on [Electron
microscope](https://en.wikipedia.org/wiki/Electron_microscope):

```
> wikiblame 'Electron microscope'
Using last 50 revisions. Use --revisions or --oldest otherwise.
Getting revisions of "Electron microscope" at en.wikipedia.org ...
Initialized empty Git repository in /tmp/tmpibe68vu1/.git/

Directory with the history as a git repository: /tmp/tmpibe68vu1
  1. Open with emacs
  2. Open with git blame
  3. Open with gitg
  4. Exit (it will remove /tmp/tmpibe68vu1)
>
```

One can run in the temporary directory (`/tmp/tmpibe68vu1` in the
example) tools like [gitg](https://wiki.gnome.org/Apps/Gitg/) to
quickly see who made what change when.

After exiting, the temporary directory is deleted.


### Different starting date

Example using a different starting date, verbose output, and selecting
git blame:

```
> wikiblame 'Electron microscope' --oldest 2020-01-01T00:00:00Z -v
Getting revisions of "Electron microscope" at en.wikipedia.org ...
  Sun Sep 22 19:58:41 2024  Alfa-ketosav      /* Main operating modes */
  Tue Aug 20 03:12:45 2024  Citation bot      Add: pmid, authors 1-1. Removed parameters. Some a
  Thu Aug  8 04:15:15 2024  JL-Bot            removing stale construction template as last edite
  Wed Jul 31 20:54:20 2024  SFBB              there was no TU-Berlin before 1946
  [...]
  Mon Jan 13 19:02:34 2020  Neurogeek         /* See also */  Quantum Microscopy
  Sun Jan 12 19:38:40 2020  Needforspeed888   Add link
Initialized empty Git repository in /tmp/tmp4fp88fcy/.git/

Directory with the history as a git repository: /tmp/tmpibe68vu1
  1. Open with emacs
  2. Open with git blame
  3. Open with gitg
  4. Exit (it will remove /tmp/tmpibe68vu1)
> 2

[...]
e7672bb2 (Materialscientist    2020-09-07 10:13:25 +0200    1) {{short description|Type of microscope with electrons as a source of
e7672bb2 (Materialscientist    2020-09-07 10:13:25 +0200    2) illumination}}
eb63cc02 (JackintheBox         2019-05-04 03:48:58 +0200    3) [[File:Electron Microscope.jpg|thumb|right|A modern transmission
eb63cc02 (JackintheBox         2019-05-04 03:48:58 +0200    4) electron microscope]][[File:Electron
[...]

>
  1. Open with emacs
  2. Open with git blame
  3. Open with gitg
  4. Exit (it will remove /tmp/tmpibe68vu1)
> 4
```


## ⚖️ License

This program is licensed under the GPL v3. See the [project
license](license.md) for further details.
