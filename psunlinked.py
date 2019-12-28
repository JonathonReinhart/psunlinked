#!/usr/bin/env python3
from __future__ import print_function
import psutil
import re
from pprint import pprint
import argparse


class Data(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __str__(self):
        return '<Data({0})>'.format(', '.join('{key}={val}'.format(key=key, val=repr(val))
            for key,val in self.__dict__.iteritems()))


def parse_mapline(line):
    # 7fbe721a4000-7fbe7235b000 r-xp 00000000 fd:01 1185241                    /usr/lib64/libc-2.21.so (deleted)
    # fs/proc/task_mmu.c    show_map_vma()
    #	seq_printf(m, "%08lx-%08lx %c%c%c%c %08llx %02x:%02x %lu ",
    #			start,
    #			end,
    #			flags & VM_READ ? 'r' : '-',
    #			flags & VM_WRITE ? 'w' : '-',
    #			flags & VM_EXEC ? 'x' : '-',
    #			flags & VM_MAYSHARE ? 's' : 'p',
    #			pgoff,
    #			MAJOR(dev), MINOR(dev), ino);
    parts = line.split(None, 5)

    addr = parts[0].split('-')
    flags = parts[1]
    dev = parts[3].split(':')

    try:
        path = parts[5].rstrip()
    except IndexError:
        path = ''
    deleted = False
    if path.endswith(' (deleted)'):
        path = path[:-10]
        deleted = True

    return Data(
        start   = int(addr[0], 16),
        end     = int(addr[1], 16),

        readable   = flags[0] == 'r',
        writable   = flags[1] == 'w',
        executable = flags[2] == 'x',
        mayshare   = flags[3] == 's',

        pgoff   = int(parts[2], 16),
        major   = int(dev[0], 16),
        minor   = int(dev[1], 16),
        inode   = int(parts[4], 10),
        path    = path,
        deleted = deleted,
        )

def read_maps(pid):
    try:
        with open('/proc/{pid}/maps'.format(pid=pid), 'r') as f:
            for line in f:
                yield parse_mapline(line)
    except IOError:
        raise psutil.AccessDenied()


def handle_proc(proc, show_files=False):
    printed_name = False

    for m in read_maps(proc.pid):
        if m.executable and m.deleted:

            if not printed_name:
                printed_name = True
                print('[{0}] {1}'.format(proc.pid, proc.name()))

            if show_files:
                print('    ' + m.path)

def parse_args():
    ap = argparse.ArgumentParser(description='Find processes executing deleted files')
    ap.add_argument('--show-files', '-f', action='store_true',
            help='Show deleted file paths')
    return ap.parse_args()


def main():
    args = parse_args()

    print('Processes executing deleted files:')
    for proc in psutil.process_iter():
        try:
            handle_proc(proc, show_files=args.show_files)
        except psutil.AccessDenied:
            continue

if __name__ == '__main__':
    main()
