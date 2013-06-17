# Copyright © 2013 Li Zhenbo
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.

import os
import sys
import shutil

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
#    print(argv_list)

if __name__ == '__main__':
    argv_list = sys.argv[1:]

    check_argv()
