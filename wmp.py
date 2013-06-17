# Copyright © 2013 Li Zhenbo
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.

import os
import sys
import shutil

#Global Config
DATA_PATH = '~/.wine_magic_prefix'

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

def get_prefix_list():
    prefix = ['~/.wine']

    if os.path.exists(DATA_PATH):
        pass
    else:   #Create one
        os.makedirs(DATA_PATH)
        print(DATA_PATH + ' created!')

    print(prefix)
    return prefix


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
