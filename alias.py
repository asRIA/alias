alias_help = """
Dynamic alias creator for system Windows.

Features:
    - execute program in fork, or in current command line
    - custom static invoke arguments

Requirements:
    - python
    - folder with script in system PATH

EXAMPLES:

1) Register this script as new alias with name 'alias':
    python {script} add alias python {script}

2) Register notepad with alias 'n':
python {script} add n notepad --fork

    If you already registered this script as an 'alias' you can use:
alias add n notepad --fork

    Now in any place you can just type:
n text.txt

    And it will work!

    Please note that --fork is important in this case.
    It will allow to invoke notepad and do not block console.
    In most cases this is useful for GUI applications.
    
"""

import argparse
import os
import sys
import textwrap

handlers = dict()
script_file = os.path.realpath(__file__)

script_dir = os.path.dirname(script_file)
drive_letter_index = script_dir.find(":")
script_dir = script_dir[:drive_letter_index].upper() + script_dir[drive_letter_index:]

def init_map():
    handlers["install"] = handle_install
    handlers["add"] = handle_add
    handlers["list"] = handle_list
    handlers["del"] = handle_rem
    handlers["rem"] = handle_rem
    handlers["get"] = handle_get


def parse_args():
    parser = argparse.ArgumentParser(prog='Alias',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(alias_help.format(script=script_file)),
                                     epilog="More info at http://github.com/asRIA/alias")

    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('install', help='Makes alias command visible globally')
    subparsers.add_parser('list', help='List current registered aliases list')

    parser_rem = subparsers.add_parser('rem', help='Remove alias with given name')
    parser_rem.add_argument('alias', nargs=1, help='Alias name')

    parser_del = subparsers.add_parser('del', help='Remove alias with given name')
    parser_del.add_argument('alias', nargs=1, help='Alias name')

    parser_get = subparsers.add_parser('get', help='Print definition for alias')
    parser_get.add_argument('alias', nargs=1, help='')

    parser_add = subparsers.add_parser('add', help='Add new alias')
    parser_add.add_argument('alias', nargs=1, help='Alias name')
    parser_add.add_argument('path', nargs=1, help='Path to executable file')
    parser_add.add_argument('args', nargs="*", help='Custom executable arguments')
    parser_add.add_argument('--fork',
                            action='store_true',
                            help="Run alias in fork of session (Useful for GUI applications).")
    parser_add.add_argument('--force', action='store_true', help='Override alias if exists')

    return vars(parser.parse_args())


def exists_alias(script_name):
    return os.path.isfile(script_name)


def get_script_name(alias):
    return os.path.join(script_dir, alias + ".bat")

def wrap_path(path):
    if path.find(" ") >= 0:
        path = "\"" + path + "\""
    return path

def handle_add(options):
    alias = options["alias"][0]
    path = wrap_path(options["path"][0])

    args = options["args"]
    fork_mode = options["fork"]
    alias_filename = get_script_name(alias)

    if not options["force"] and exists_alias(alias_filename):
        print("Alias '%s' already exists." % alias)
        return 1

    content_header = "@echo off\n"
    content_args = ""
    if fork_mode:
        content_command_template = "start \"\" {path}{args} %*"
    else:
        content_command_template = "call {path}{args} %*"

    for arg in args:
        arg = wrap_path(arg)
        content_args += " {arg}".format(arg=arg)

    content = content_header + content_command_template.format(path=path, args=content_args)

    alias_file = open(alias_filename, "w")
    alias_file.write(content)
    alias_file.close()

    print("'{alias}' has been added in {mode} mode".format(alias=alias, mode="fork" if fork_mode else "normal"))


def handle_list(options):
    files = os.listdir(script_dir)
    aliases = ""
    aliases_count = 0
    for file in files:
        file_path = os.path.join(script_dir, file)
        if os.path.isfile(file_path):
            dot_index = file.rfind(".")
            file_name = file[:dot_index]
            extension = file[dot_index+1:]
            extension = extension.lower()
            if extension == "bat":
                aliases_count += 1
                aliases += "- " + file_name + "\n"
    if aliases_count > 0:
        print("Found %d registered aliases:" % aliases_count)
        print(aliases)
    else:
        print("There is no registered aliases")


def handle_get(options):
    alias = options["alias"][0]
    alias_filename = get_script_name(alias)

    if not exists_alias(alias_filename):
        print("'%s' doesn't exist" % alias)
        return 1
    alias_file = open(alias_filename, "r")
    print(alias_file.read())
    return 0


def handle_rem(options):
    alias = options["alias"][0]
    alias_filename = get_script_name(alias)

    if not exists_alias(alias_filename):
        print("'%s' doesn't exist" % alias)
        return 1

    os.remove(alias_filename)
    print("'%s' has been removed" % alias)
    return 0
    
def handle_install(options):
    if not check_integration():
        subprocess.Popen('setx PATH "%PATH%;{path}"'.format(path=script_dir), shell=True).communicate()
        subprocess.call([sys.executable, script_file, "add", "alias", sys.executable, script_file], shell=True)
        
def check_integration():
    paths = os.environ["PATH"].split(";")
    script_dir_formatted = script_dir
    if script_dir_formatted not in paths:
        print("Aliases dir is not registered in system PATH, please modify user env variables by adding:")
        print(script_dir_formatted)
        return False
    return True

if __name__ == '__main__':

    init_map()
    args = parse_args()
    check_integration()

    if args["command"] in handlers:
        errcode = handlers[args["command"]](args)
    else:
        print('Missing command, please run with -h for help')
        errcode = 1
    exit(errcode)



