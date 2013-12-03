#!/usr/bin/python3

import os, sys, shutil, argparse

#Global Config
DATA_PATH = os.path.expanduser('~/.wine_magic_prefix')
PREFIX_PATH = os.path.expanduser('~/.wine')
COMMENT_FILE = '.comment'


def yes_or_no(hint = ''):
    inp = input(hint + '[y/n]?')
    c = inp.strip()[0]
    return c == 'y' or c == 'Y'

def get_absolute_path(x):
    '''x is the relative path

    Return the absolute path
    '''
    return (DATA_PATH+'/' + x)

def write_comment(path, comment='Untitled'):
    file_path = path + '/' + COMMENT_FILE
    #Need test, and need to be more pythonic
    if os.path.isfile(file_path):
        flag = yes_or_no('Do you want to overwrite old comment: \n\'' + get_comment(path) + '\' ')
    else:
        flag = True

    if not flag:
        return
    with open(file_path, 'w', encoding='utf-8') as fout:
        comment = comment.strip()
        comment.replace('\n', '  ')
        fout.write(comment)

def get_comment(path):
    '''path should be an absolute path to a folder(I won't check it here)
    return a string(should not have \n symbols
    '''
    file_path = path + '/' + COMMENT_FILE
    try:
        with open(file_path, 'r', encoding='utf-8') as fin:
            comment = fin.read()
            comment = comment.strip()
            comment.replace('\n', '  ')
    except FileNotFoundError:
        #with open(file_path, 'w', encoding='utf-8') as fout:
        print('Auto create a .comment file for  ' + path)
        write_comment(path)
        comment = 'Untitled'
    return comment

def get_prefix_list():
    '''Return a list, all the prefixes are included.
       example: [(folder_name1, comment1), (folder_name2, comment2)]
    '''
    prefix = []
    if os.path.isdir(PREFIX_PATH):  #Not so pythonic,but useful
        prefix.append(('.wine', get_comment(PREFIX_PATH)))

    try:
        prefix += [ (path,get_comment(get_absolute_path(path)) ) for path in os.listdir(DATA_PATH)]
    except FileNotFoundError:
        print('Auto create DATA_PATH: ' + DATA_PATH)
        os.mkdir(DATA_PATH)

    return prefix

def show_prefix_list():
    global prefix_list
    for c in prefix_list:
        print(c)

def backup(dst):
    assert os.path.isdir(PREFIX_PATH)
    dst = get_absolute_path(dst)
    shutil.move(PREFIX_PATH, dst)

def copyto(dst):
    assert os.path.isdir(PREFIX_PATH)
    dst = get_absolute_path(dst)
    shutil.copytree(PREFIX_PATH, dst, True)

def use_prefix(src):
    #Next feature: auto-load some commands from shell
    global prefix_list

    print('protect function is a stub')

    src0 = src
    src = get_absolute_path(src)
    try:
        shutil.move(src, PREFIX_PATH)
    except FileExistsError:
        #Assume that prefix_list[0] means .wine
        if yes_or_no('trying to overwrite ' +  str(prefix_list[0])):
            clean_prefix()
            use_from(src0)
        else:
            print('Don\'t overwrite, aborting')

def use_from(src):
    global prefix_list

    print('protect function is a stub')

    src0 = src
    src = get_absolute_path(src)
    try:
        shutil.copytree(src, PREFIX_PATH, True)
    except FileExistsError:
        #Assume that prefix_list[0] means .wine
        if yes_or_no('trying to overwrite ' +  str(prefix_list[0])):
            clean_prefix()
            use_from(src0)
        else:
            print('Don\'t overwrite, aborting')

def delete_prefix(obj):
    path = get_absolute_path(obj)
    shutil.rmtree(path)

def clean_prefix():
    try:
        shutil.rmtree(PREFIX_PATH)
    except FileNotFoundError:
        print('FileNotFound, Skip')

def _handle_args():
    praser = argparse.ArgumentParser(prog='WineMagicPrefix', description='Manage wine prefix in a simple way.')

    praser.add_argument('-l', '--list', action='store_true')

    #You can only use it like '--delete prefix_a --delete prefix_b', and I don't know how to make it better
    praser.add_argument('-d', '--delete', action='append')

    praser.add_argument('-b','--backup', action='store')
    praser.add_argument('-t','--copy-to', action='store')

    praser.add_argument('-u', '--use', action='store')
    praser.add_argument('-f', '--use-from', action='store')

    praser.add_argument('-p', '--protect', action='append')  #same problem with --delete

    praser.add_argument('-c', '--clean', action='store_true')

    praser.add_argument('-s', '--say', action='store')


    arg_result = vars(praser.parse_args(sys.argv[1:]))
    arg_set = set(key for key, val in arg_result.items() if val)

    return (arg_result, arg_set)

if __name__ == '__main__':
    arg_result, arg_set = _handle_args()

    if 'say' in arg_set:
        write_comment(PREFIX_PATH, arg_result['say'])
    if 'clean' in arg_set:
        clean_prefix()

    prefix_list = get_prefix_list()

    if 'list' in arg_set:
        show_prefix_list()
    if 'backup' in arg_set:
        backup(arg_result['backup'])

    if 'copy_to' in arg_set:
        copyto(arg_result['copy_to'])

    if 'use' in arg_set:
        use_prefix(arg_result['use'])
    if 'use_from' in arg_set:
        use_from(arg_result['use_from'])

    if 'delete' in arg_set:
        for prefix in arg_result['delete']:
            delete_prefix(prefix)

    if 'protect' in arg_set:
        print ('STUB now')

