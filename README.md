psunlinked
==========

Find processes executing deleted files

## Overview
On Linux (and likely other UNIX-like OSes), when a file is "deleted", it is
really only "unlinked" from the filesystem; the file's contents persist until
there are no more references to it. This allows for executable files (programs
and shared libraries) to be updated while processes are running, and also
allows a program to delete itself and continue executing. This script helps to
identify processes executing with pages mapped to files that have been deleted.

This utility was inspired by the `zypper ps` command on SuSE Linux.

## Requirements:
- [`psutil`](https://github.com/giampaolo/psutil)

## License
This software is released under the [MIT License](https://opensource.org/licenses/MIT).
