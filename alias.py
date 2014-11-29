import argparse
import os

handlers = dict()
script_file = os.path.realpath(__file__)
script_dir = os.path.dirname(script_file)

def init_map():
    handlers["add"] = handle_add
    handlers["list"] = handle_list
    handlers["del"] = handle_rem
    handlers["rem"] = handle_rem
    handlers["get"] = handle_get


def parse_args():
    parser = argparse.ArgumentParser(prog='Alias',
                                     description="Dynamic alias creator for system windows",
                                     epilog="moar info at http://github.com/asRIA/alias")

    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='')

    parser_rem = subparsers.add_parser('rem', help='')
    parser_rem.add_argument('alias', nargs=1, help='')

    parser_del = subparsers.add_parser('del', help='')
    parser_del.add_argument('alias', nargs=1, help='')

    parser_get = subparsers.add_parser('get', help='')
    parser_get.add_argument('alias', nargs=1, help='')

    parser_add = subparsers.add_parser('add', help='')
    parser_add.add_argument('alias', nargs=1, help='')
    parser_add.add_argument('path', nargs=1, help='')
    parser_add.add_argument('args', nargs="*", help='')

    return vars(parser.parse_args())


def exists_alias(script_name):
    return os.path.isfile(script_name)


def get_script_name(alias):
    return os.path.join(script_dir, alias + ".bat")


def handle_add(options):
    alias = options["alias"][0]
    path = options["path"][0]
    args = options["args"]
    alias_filename = get_script_name(alias)

    if exists_alias(alias_filename):
        print("Alias '%s' already exists." % alias)
        return 1

    content = "@echo off\n"
    content += "call "
    content += '"%s" ' % path
    for arg in args:
        content += '"%s" ' % arg
    content += '%* '

    alias_file = open(alias_filename, "w")
    alias_file.write(content)
    alias_file.close()

    print("'%s' has been added" % alias)


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
                aliases_count+=1
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


if __name__ == '__main__':
    errcode = 1
    init_map()
    args = parse_args()

    print(args)
    if args["command"] in handlers:
        errcode = handlers[args["command"]](args)
    else:
        print('nope')
    exit(errcode)



