#!/usr/bin/python3

import os, sys, shutil, argparse

#Global Config
DATA_PATH = os.path.expanduser('~/.wine_magic_prefix')
PREFIX_PATH = os.path.expanduser('~/.wine')
PROTECT_FLAG = '[[Protect]]'
COMMENT_FILE = '.comment'


def is_protected(prefix):
    '''prefix is a string
    '''
    return prefix[- len(PROTECT_FLAG) : ] == PROTECT_FLAG

def get_absolute_path(x):
    '''x is the relative path

    Return the absolute path
    '''
    return (DATA_PATH+'/' + x)

def get_comment(path):
    '''path should be an absolute path to a folder(I won't check it here)
    return a string(should not have \n symbols
    '''
    file_path = path + '/' + COMMENT_FILE
    with open(file_path, 'r', encoding='utf-8') as fin:
        comment = fin.read()
        comment = comment.strip()
        comment.replace('\n', '  ')
    return comment

def write_comment(path, comment='Untitled'):
    file_path = path + '/' + COMMENT_FILE
    with open(file_path, 'w', encoding='utf-8'):
        comment = comment.strip()
        comment.replace('\n', '  ')
        fout.write(comment)

def get_prefix_list():
    '''Return a list, all the prefixes are included.
       example: [(folder_name1, comment1), (folder_name2, comment2)]
    '''
    prefix = []
    if os.path.isdir(PREFIX_PATH):
        try:
            prefix.append(('.wine', get_comment(PREFIX_PATH)))
        except IOError:
            print('Auto create a .comment file for .wine')
            write_comment(PREFIX_PATH)

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

def yes_or_no(hint = ''):
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

    if is_protected(argv_list[1]):
        flag = yes_or_no("Use a protected prefix")
        if not flag:
            print("Can't use a protected prefix. Aborted.")
            exit()

    try_to_overwrite(PREFIX_PATH)

    src = get_absolute_path(argv_list[1])
    shutil.move(src, PREFIX_PATH)

def use_prefix_new():
    global argv_list
    global prefix_list

    if argv_list[1] not in prefix_list:
        raise ValueError('Can\'t find prefix:  ' + argv_list[1])

    try_to_overwrite(PREFIX_PATH)

    src = get_absolute_path(argv_list[1])
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

def delete_prefix():
    paths = get_path_list()
    if (len(paths) == 0):
        print('Nothing to do.')
        return

    hint = 'Are you going to delete: ' + str(argv_list[1:])
    flag = yes_or_no(hint)
    if flag:
        for path in paths:
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
    praser.add_argument('--backup-to', action='store')

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

    #if '-b' in argv_list:
        #backup()
    #elif '-bn' in argv_list:
        #backup_new()
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
