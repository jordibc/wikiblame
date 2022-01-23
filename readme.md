# Wikiblame

Convert a wikipedia article to a git repository and explore it with emacs in
version control mode (vs-annotate). Optionally run gitk and git blame too.

This is a much nicer way to find out where certain changes happened in a wiki
page.


## Usage

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

## Examples

### Simple use

In this example we see the history of the article on [Electron
microscope](https://en.wikipedia.org/wiki/Electron_microscope):

```
> ./wikiblame.py 'Electron microscope'
Initialized empty Git repository in /tmp/tmp7fccmxs8/.git/
[master (root-commit) 83f5932] /* Scanning electron microscope (SEM) */ link
 Author: Iztwoz <no email>
 Date: Sun Jan 6 12:32:07 2019 +0100
 1 file changed, 903 insertions(+)
 create mode 100644 article
[master 20b0990] Alter: doi-broken-date. | You can [[WP:UCB|use this bot]] yourself. [[WP:DBUG|Report bugs here]]. | [[WP:UCB|User-activated]].
 Author: Citation bot <no email>
 Date: Tue Jan 8 03:31:48 2019 +0100
 1 file changed, 2 insertions(+), 2 deletions(-)
[master 4625c2f] [[User:JCW-CleanerBot#Logic|task]], replaced: J. Microscopy → Journal of Microscopy
 Author: JCW-CleanerBot <no email>
 Date: Fri Jan 18 02:39:15 2019 +0100
 1 file changed, 12 insertions(+), 12 deletions(-)

[...]

[master 6b67d5c] Rescuing 1 sources and tagging 0 as dead.) #IABot (v2.0.8.6
 Author: InternetArchiveBot <no email>
 Date: Tue Jan 11 00:22:08 2022 +0100
 1 file changed, 5 insertions(+), 2 deletions(-)

Directory with the history as a git repository: /tmp/tmp7fccmxs8
Press enter to remove the temporal directory...
```

One can go into the temporary directory (`/tmp/tmp7fccmxs8` in the example)
and use tools like [gitg](https://wiki.gnome.org/Apps/Gitg/) to quickly
see who made what change when.

After pressing enter on the console, the temporary directory is deleted.

### Different starting date

To see it from a different starting date, and launching the gitk tool and
seeing directly a `git blame` on the screen:

```
> ./wikiblame.py 'Electron microscope' --start 2017-01-01T00:00:00Z --gitk --git-blame
Initialized empty Git repository in /tmp/tmp4fp88fcy/.git/
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
```

And after quitting the `git blame` session:

```
Directory with the history as a git repository: /tmp/tmp4fp88fcy
Press enter to remove the temporal directory...
```
