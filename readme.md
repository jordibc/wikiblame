# Wikiblame

Convert a wikipedia article to a git repository.

Then, offer to explore it with emacs in version control mode
(vc-annotate), or with git blame, or gitg.

This is a much nicer way to find out where certain changes happened in
a wiki page.


## Dependencies

Wikiblame uses the [mwclient](https://github.com/mwclient/mwclient)
module to communicate with the MediaWiki API.

It is packaged in most systems (for example, as `python3-mwclient` in
Debian), but you can also install it with:

```sh
pip install mwclient
```


## Usage

```
usage: wikiblame.py [-h] [--start START] [--end END] [--site SITE] [-v] article

positional arguments:
  article        name of the wikipedia article

options:
  -h, --help     show this help message and exit
  --start START  oldest revision date (default: 2022-01-01T00:00:00Z)
  --end END      newest revision date (latest revision if not set)
  --site SITE    wikimedia site to access (default: en.wikipedia.org)
  -v, --verbose  show commit messages
```


## Examples

### Simple use

In this example we see the history of the article on [Electron
microscope](https://en.wikipedia.org/wiki/Electron_microscope):

```
> ./wikiblame.py 'Electron microscope'
Initialized empty Git repository in /tmp/tmpibe68vu1/.git/
Adding revisions...

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
> ./wikiblame.py 'Electron microscope' --start 2017-01-01T00:00:00Z -v
Initialized empty Git repository in /tmp/tmp4fp88fcy/.git/
Adding revisions...
[master (root-commit) 9e8ac23] hhhhhhhhhhh
 Author: 84.21.150.53 <no email>
 Date: Mon Jan 23 14:20:28 2017 +0100
 1 file changed, 796 insertions(+)
 create mode 100644 article
[master b97c5c7] Reverted edits by [[Special:Contribs/84.21.150.53|84.21.150.53]] ([[User talk:84.21.150.53|talk]]) to last version by Serols
 Author: Quinton Feldberg <no email>
 Date: Mon Jan 23 14:21:35 2017 +0100
 1 file changed, 13 insertions(+), 13 deletions(-)

[...]

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
f36fa7f5 (Andy Dingley         2017-09-18 11:03:24 +0200    5) Microscope.png|right|thumb|Diagram of a transmission electron
f36fa7f5 (Andy Dingley         2017-09-18 11:03:24 +0200    6) microscope]]
d3068b3d (ClueBot NG           2019-06-14 16:44:32 +0200    7) [[File:Ernst Ruska Electron Microscope - Deutsches Museum -
f36fa7f5 (Andy Dingley         2017-09-18 11:03:24 +0200    8) Munich-edit.jpg|thumb|right|Electron microscope constructed by
f36fa7f5 (Andy Dingley         2017-09-18 11:03:24 +0200    9) [[Ernst Ruska]] in 1933]]
9ee5f1eb (47.15.144.188        2018-10-03 04:59:56 +0200   10)
0f4b5414 (Gobonobo             2020-11-24 11:18:24 +0100   11) An '''electron microscope''' is a [[microscope]] that uses a beam of
63b13ce1 (Materialscientist    2020-09-07 10:14:10 +0200   12) accelerated [[electron]]s as a source of illumination. As the
d1b67ce3 (NeedsGlasses         2020-07-23 05:06:59 +0200   13) wavelength of an electron can be up to 100,000 times shorter than
0887c315 (Pelirojopajaro       2019-11-25 14:29:21 +0100   14) that of visible light [[photon]]s, electron microscopes have a higher
8bc9528b (Materialscientist    2018-11-03 09:34:47 +0100   15) [[Angular resolution|resolving power]] than [[optical
8bc9528b (Materialscientist    2018-11-03 09:34:47 +0100   16) microscope|light microscope]]s and can reveal the structure of
8bc9528b (Materialscientist    2018-11-03 09:34:47 +0100   17) smaller objects. A [[scanning transmission electron microscope]] has
e7672bb2 (Materialscientist    2020-09-07 10:13:25 +0200   18) achieved better than 50&nbsp;[[Picometre|pm]] resolution in [[annular

[...]

Directory with the history as a git repository: /tmp/tmpibe68vu1
1. Open with emacs
2. Open with git blame
3. Open with gitg
4. Exit (it will remove /tmp/tmpibe68vu1)
> 4
```
