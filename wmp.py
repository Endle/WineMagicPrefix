#!/usr/bin/python3
# Copyright © 2013 Li Zhenbo
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.

import os
import sys
import shutil

#Global Config
DATA_PATH = os.path.expanduser('~/.wine_magic_prefix')
PREFIX_PATH = os.path.expanduser('~/.wine')
PROTECT_FLAG = "[[Protect]]"

def check_argv():
    """Check if the argv has only one option
    """
    global argv_list
    count = 0
    for s in argv_list:
        if s[0] == '-':
            count += 1

    if count != 1:
        print (argv_list)
        raise ValueError('Wrong Command')

def get_absolute_path(x):
    """x is the relative path

    Return the absolute path
    """
    return (DATA_PATH+'/' + x)

def get_prefix_list():
    """Return a list, all the prefixes are included.
    """
    prefix = []
    if os.path.isdir(PREFIX_PATH):
        prefix.append('.wine')

    #Make sure DATA_PATH is fine
    if os.path.exists(DATA_PATH):
        if not os.path.isdir(DATA_PATH):
            raise OSError(DATA_PATH + ' not a folder')
    else:   #Create one
        try:
            os.makedirs(DATA_PATH)
            print(DATA_PATH + ' created!')
        except OSError:
            print('Can\'t create ' + DATA_PATH)
            exit()

    for x in os.listdir(DATA_PATH) : 
        #        print( get_absolute_path(x) )
        prefix.append(x)

    return prefix

def show_prefix_list():
    global prefix_list
    for c in prefix_list:
        print(c)

def yes_or_no(hint = ""):
    inp = input(hint + '[y/n]?')
    c = inp.strip()[0]
    return c == 'y' or c == 'Y'

def try_to_overwrite(path):
    """Over-write path if the user confirms that
    """
    if os.path.exists(path):
        flag = yes_or_no("Over-write " + path)
        if flag:
            shutil.rmtree(PREFIX_PATH)
        else:
            print("Aborted.")
            exit()


def backup():
    if not os.path.isdir(PREFIX_PATH):
        raise OSError('Nothing to backup!')
    
    global argv_list
    dst = get_absolute_path(argv_list[1])
    try_to_overwrite(dst)
    shutil.move(PREFIX_PATH, dst)

def backup_new():
    if not os.path.isdir(PREFIX_PATH):
        raise OSError('Nothing to backup!')
    
    global argv_list
    dst = get_absolute_path(argv_list[1])
    try_to_overwrite(dst)
    shutil.copytree(PREFIX_PATH, dst, True)

def use_prefix():
    global argv_list
    global prefix_list 
    
    if argv_list[1] not in prefix_list:
        raise ValueError("Can't find prefix:  " + argv_list[1])

    try_to_overwrite(PREFIX_PATH)

    src = get_absolute_path(argv_list[1])
    shutil.move(src, PREFIX_PATH)

def use_prefix_new():
    global argv_list
    global prefix_list 
    
    if argv_list[1] not in prefix_list:
        raise ValueError("Can't find prefix:  " + argv_list[1])

    try_to_overwrite(PREFIX_PATH)

    src = get_absolute_path(argv_list[1])
    shutil.copytree(src, PREFIX_PATH, True)

def delete_prefix():
    global argv_list
    paths = []
    for prfx in argv_list[1:]:
        path = get_absolute_path(prfx)
        if os.path.exists(path):
            paths.append(path)
        else:
            print(prfx + ' not exists. Ignore it')
            argv_list.remove(prfx)

    if (len(paths) == 0):
        print('Nothing to do.')
        return

    hint = 'Are you going to delete: ' + str(argv_list[1:])
    flag = yes_or_no(hint)
    if flag:
        for path in paths:
            shutil.rmtree(path)

if __name__ == '__main__':
    argv_list = sys.argv[1:]

    check_argv()

    prefix_list = get_prefix_list()

    if '-b' in argv_list:
        backup()
    elif '-bn' in argv_list:
        backup_new()
    elif '-u' in argv_list:
        use_prefix()
    elif '-un' in argv_list:
        use_prefix_new()
    elif '-l' in argv_list:
        show_prefix_list()
    elif '-d' in argv_list:
        delete_prefix()
    else:
        print(argv_list)
        raise ValueError('Invalid Option!')
