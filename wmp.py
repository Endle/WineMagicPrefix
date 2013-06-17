# Copyright © 2013 Li Zhenbo
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.

import os
import sys
import shutil

#Global Config
DATA_PATH = os.path.expanduser('~/.wine_magic_prefix')

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
    return (DATA_PATH+'\\' + x)

def get_prefix_list():
    """Return a list, all the prefixes are included.
    """
    prefix = ['~/.wine']

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
    inp = inp.strip().lowercase()
    return inp[0] == 'y'

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
    else:
        print(argv_list)
        raise ValueError('Invalid Option!')
