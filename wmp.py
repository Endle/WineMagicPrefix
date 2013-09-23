#!/usr/bin/python3

import os, sys, shutil, argparse

#Global Config
DATA_PATH = os.path.expanduser('~/.wine_magic_prefix')
PREFIX_PATH = os.path.expanduser('~/.wine')
PROTECT_FLAG = '[[Protect]]'
COMMENT_FILE = '.comment'


def yes_or_no(hint = ''):
    inp = input(hint + '[y/n]?')
    c = inp.strip()[0]
    return c == 'y' or c == 'Y'

def is_protected(prefix):
    '''prefix is a string
    '''
    return prefix[- len(PROTECT_FLAG) : ] == PROTECT_FLAG

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
        prefix += os.listdir(DATA_PATH)
    except FileNotFoundError:
        print('Auto create DATA_PATH: ' + DATA_PATH)
        os.mkdir(DATA_PATH)

    print(prefix)
    return prefix

def show_prefix_list():
    global prefix_list
    for c in prefix_list:
        print(c)

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

def backup(dst):
    assert os.path.isdir(PREFIX_PATH)
    dst = get_absolute_path(dst)
    shutil.move(PREFIX_PATH, dst)

def copyto(dst):
    assert os.path.isdir(PREFIX_PATH)
    dst = get_absolute_path(dst)
    print(dst)
    shutil.copytree(PREFIX_PATH, dst, True)

def use_prefix(src):
    #Next feature: auto-load some commands from shell
    global prefix_list
    assert src in prefix_list

    print('protect function is a stub')

    src = get_absolute_path(src)
    if os.path.isdir(PREFIX_PATH):
        raise FileExistsError
    #Should be handled in a better way
    shutil.move(src, PREFIX_PATH)

def use_from(src):
    global prefix_list
    assert src in prefix_list

    print('protect function is a stub')

    src = get_absolute_path(src)
    if os.path.isdir(PREFIX_PATH):
        raise FileExistsError
    #Should be handled in a better way
    shutil.copytree(src, PREFIX_PATH, True)

def get_path_list():
    global argv_list
    paths = []
    for prfx in argv_list[1:]:
        path = get_absolute_path(prfx)
        if os.path.exists(path):
            paths.append(path)
        else:
            print(prfx + ' not exists. Ignore it')
            argv_list.remove(prfx)
    return paths

def delete_prefix(obj):
    path = get_absolute_path(obj)
    shutil.rmtree(path)

def clean_prefix():
    shutil.rmtree(PREFIX_PATH)

def protect():
    global argv_list
    paths = get_path_list()
    if (len(paths) == 0):
        print('Nothing to do.')
        return
    for path in paths:
        shutil.move(path, path+PROTECT_FLAG)

def use_protect():
    global argv_list
    if (argv_list[1]+PROTECT_FLAG) not in prefix_list:
        raise ValueError('No such prefix')

    argv_list[1] = argv_list[1] + PROTECT_FLAG
    use_prefix_new()

def _handle_args():
    praser = argparse.ArgumentParser(prog='WineMagicPrefix', description='Manage wine prefix in a simple way.')

    praser.add_argument('--list', action='store_true')

    #You can only use it like '--delete prefix_a --delete prefix_b', and I don't know how to make it better
    praser.add_argument('--delete', action='append')

    praser.add_argument('--backup', action='store')
    praser.add_argument('--copy-to', action='store')

    praser.add_argument('--use', action='store')
    praser.add_argument('--use-from', action='store')

    praser.add_argument('--protect', action='append')  #same problem with --delete

    praser.add_argument('--clean', action='store_true')

    praser.add_argument('--add', action='append')


    arg_result = vars(praser.parse_args(sys.argv[1:]))
    arg_set = set(key for key, val in arg_result.items() if val)

    return (arg_result, arg_set)

if __name__ == '__main__':
    arg_result, arg_set = _handle_args()
    print(arg_result)
    print(arg_set)


    prefix_list = get_prefix_list()

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
    #elif '-u' in argv_list:
        #use_prefix()
    #elif '-un' in argv_list:
        #use_prefix_new()
    #elif '-l' in argv_list:
        #show_prefix_list()
    #elif '-d' in argv_list:
        #delete_prefix()
    #elif '-p' in argv_list:
        #protect()
    #elif '-up' in argv_list:
        #use_protect()
    #elif '-c' in argv_list:
        #clean_prefix()
    #else:
        #print(argv_list)
        #raise ValueError('Invalid Option!')
