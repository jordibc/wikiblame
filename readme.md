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
usage: wikiblame.py [-h] [-n N] [--oldest TIMESTAMP] [--newest TIMESTAMP] [--site SITE] [-v] article

positional arguments:
  article        name of the wikipedia article

options:
  -h, --help          show this help message and exit
  -n N, --revisions N  number of revisions
  --revisions N       number of revisions
  --oldest TIMESTAMP  oldest revision, like 2022-01-01T00:00:00Z
  --newest TIMESTAMP  newest revision (latest if not set)
  --site SITE         wikimedia site to access
  -v, --verbose       show retrieved revisions
```


## Examples

### Simple use

In this example we see the history of the article on [Electron
microscope](https://en.wikipedia.org/wiki/Electron_microscope):

```
> ./wikiblame.py 'Electron microscope'
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
> ./wikiblame.py 'Electron microscope' --oldest 2020-01-01T00:00:00Z -v
Getting revisions of "Electron microscope" at en.wikipedia.org ...
  Sun Sep 22 19:58:41 2024  Alfa-ketosav      /* Main operating modes */
  Tue Aug 20 03:12:45 2024  Citation bot      Add: pmid, authors 1-1. Removed parameters. Some a
  Thu Aug  8 04:15:15 2024  JL-Bot            removing stale construction template as last edite
  Wed Jul 31 20:54:20 2024  SFBB              there was no TU-Berlin before 1946
  Tue Jul 30 06:18:13 2024  Unknown cow       fix typo in word "produced"
  Fri Jul 26 15:26:53 2024  129.7.106.20      /* Sample preparation for TEM */ formatted citatio
  Fri Jul 19 07:40:25 2024  WikiCleanerBot    v2.05b - [[User:WikiCleanerBot#T20|Bot T20 CW#61]]

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
