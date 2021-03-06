#!/usr/bin/env python3
"""
The MIT License (MIT)

Copyright (c) 2013-2015  Zhenbo Li

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os, sys, shutil, argparse

#Global Config
DATA_PATH = os.path.expanduser('~/.wine_magic_prefix')
PREFIX_PATH = os.path.expanduser('~/.wine')
COMMENT_FILE = '.comment'
CLIPBOARD_FILE = ".clipboard"
DEFAULT_COMMENT = 'Untitled'


def yes_or_no(hint=''):
    inp = input(hint + '[y/n]?')
    c = inp.strip()[0]
    return c == 'y' or c == 'Y'

def get_absolute_path(x):
    '''x is the relative path

    Return the absolute path
    '''
    return DATA_PATH + '/' + x

def strip_str(s):
    s = s.strip()
    s.replace('\n', ' ')
    return s

def write_to_file(path, file_name, str_to_write,
        default_str="", get_old_text=lambda x,y:""):
    file_path = path + '/' + file_name
    #Need test, and need to be more pythonic
    if os.path.isfile(file_path) \
        and get_old_text(path, file_name) != default_str:
        flag = yes_or_no('Do you want to overwrite old content: \n\''
                         + get_old_text(path, file_name) + '\' ')
    else:
        flag = True

    if flag:
        with open(file_path, 'w', encoding='utf-8') as fout:
            str_to_write = strip_str(str_to_write)
            fout.write(str_to_write)

def read_from_file(path, file_name, quietCreate=False, default_str=""):
    file_path = path + '/' + file_name
    try:
        with open(file_path, 'r', encoding='utf-8') as fin:
            input_str = strip_str(fin.read())
    except FileNotFoundError:
        if not quietCreate:
            print(file_name + "File Not Found")
            return default_str
        print("Auto create " + file_name + "file for "+ path)
        write_to_file(path, file_name, default_str)
        input_str = default_str
    return input_str

def write_comment(path, comment=DEFAULT_COMMENT):
    write_to_file(path, COMMENT_FILE, comment,
        default_str = DEFAULT_COMMENT, get_old_text=read_from_file)

def get_comment(path, quietCreate=False):
    return read_from_file(path, COMMENT_FILE, quietCreate, default_str=DEFAULT_COMMENT)

def load_clipboard(path=PREFIX_PATH):
    clip = read_from_file(path, CLIPBOARD_FILE, False)
    if clip:
        import pyperclip
        pyperclip.copy(clip)

def save_clipboard(path, clip):
    write_to_file(path, CLIPBOARD_FILE, clip, get_old_text=read_from_file)

def get_prefix_list():
    '''Return a dict, all the prefixes are included.
       example: {folder_name_i: comment_i}
    '''
    prefix = {}
    if os.path.isdir(PREFIX_PATH):  #Not so pythonic,but useful
        prefix['.wine'] = get_comment(PREFIX_PATH)

    try:
        paths = os.listdir(DATA_PATH)
    except:
        print('Auto create DATA_PATH: ' + DATA_PATH)
        os.mkdir(DATA_PATH)
        paths = os.listdir(DATA_PATH)

    for path in paths:
        prefix[path] = get_comment(get_absolute_path(path))

    return prefix

def show_prefix_list():
    global prefix_list
    try:
        width = max([len(c) for c in prefix_list.keys()])
    except ValueError:
        width = 0
    output = ["{0:{2}} :  {1}".format(c, prefix_list[c], width)
                for c in prefix_list.keys()]
    output.sort()
    for s in output:
        print(s)

def backup(dst):
    assert os.path.isdir(PREFIX_PATH)
    dst = get_absolute_path(dst)
    shutil.move(PREFIX_PATH, dst)

def copyto(dst):
    assert os.path.isdir(PREFIX_PATH)
    dst = get_absolute_path(dst)
    shutil.copytree(PREFIX_PATH, dst, True)

def use_prefix(src):
    global prefix_list

    src = get_absolute_path(src)
    if os.path.isdir(PREFIX_PATH):
        raise FileExistsError
    #Should be handled in a better way
    shutil.move(src, PREFIX_PATH)
    load_clipboard()

def use_from(src):
    global prefix_list

    src = get_absolute_path(src)
    if os.path.isdir(PREFIX_PATH):
        raise FileExistsError
    #Should be handled in a better way
    shutil.copytree(src, PREFIX_PATH, True)

def delete_prefix(obj):
    path = get_absolute_path(obj)
    shutil.rmtree(path)

def clean_prefix():
    try:
        current = get_comment(PREFIX_PATH, True)
        if current == DEFAULT_COMMENT or yes_or_no("Do you want to delete " + current):
            shutil.rmtree(PREFIX_PATH)
        else:
            print("clean_prefix refused.")
            return
    except FileNotFoundError:
        print('FileNotFound, Skip')

def _handle_args():
    praser = argparse.ArgumentParser(prog='WineMagicPrefix',
                    description='Manage wine prefix in a simple way.')

    praser.add_argument('-l', '--list', action='store_true')

    praser.add_argument('-d', '--delete', nargs='+')

    praser.add_argument('-b', '--backup', action='store')
    praser.add_argument('-bs', '--backup_as_say', action='store_true')
    praser.add_argument('-t', '--copy-to', action='store')

    praser.add_argument('-u', '--use', action='store')
    praser.add_argument('-f', '--use-from', action='store')

    praser.add_argument('-c', '--clean', action='store_true')

    praser.add_argument('-s', '--say', action='store')
    praser.add_argument('-x', '--set_clip', action='store')
    praser.add_argument('-lx', '--load_clip', action='store_true')

    arg_result = vars(praser.parse_args(sys.argv[1:]))
    arg_set = set(key for key, val in arg_result.items() if val)

    return (arg_result, arg_set)

if __name__ == '__main__':
    arg_result, arg_set = _handle_args()

    if 'say' in arg_set:
        write_comment(PREFIX_PATH, arg_result['say'])
    if 'set_clip' in arg_set:
        save_clipboard(PREFIX_PATH, arg_result['set_clip'])
    if 'load_clip' in arg_set:
        load_clipboard()
    if 'clean' in arg_set:
        clean_prefix()

    prefix_list = get_prefix_list()

    if 'list' in arg_set:
        show_prefix_list()
    if 'backup' in arg_set:
        backup(arg_result['backup'])

    if 'copy_to' in arg_set or 'use_from' in arg_set:
        import pyfastcopy

    if 'copy_to' in arg_set:
        copyto(arg_result['copy_to'])

    if 'use' in arg_set:
        use_prefix(arg_result['use'])
    if 'use_from' in arg_set:
        use_from(arg_result['use_from'])

    if 'delete' in arg_set:
        for prefix in arg_result['delete']:
            delete_prefix(prefix)

    if 'backup_as_say' in arg_set:
        assert('backup' not in arg_set)
        backup(prefix_list['.wine'])

