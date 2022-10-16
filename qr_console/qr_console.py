"""
module provides a console application builder based on argparse library
"""

import argparse
import re

import colorama
from colorama import Fore, Style
import sys


colorama.init()


class QRHelpAction(argparse.Action):
    """redefining help action from argparse module to avoid finishing app after help message"""
    def __init__(self,
                 option_strings,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help=None):
        super(QRHelpAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()


argparse._HelpAction = QRHelpAction


class ThrowingArgumentParser(argparse.ArgumentParser):
    class ArgumentParserError(Exception):
        pass

    def error(self, message):
        raise self.ArgumentParserError(message)


class QRCommand:
    def __init__(self, name: str, func=None, help: str = None):
        self.name, self.help = name, help
        self.arguments = dict()
        self.func = func

    def add_argument(self, name, *args, **kwargs):
        """provides a wrap over 'parser.add_argument' function from argparse library. Usage examples:
        add_argument('-c', '--config', type=str, default='config.yaml', help='configuration file')
        add_argument('-f', '--flag', action='store_true', help='raise some flag');
        Note: 'name' parameter must be set either with leading '-' or '--' (like '-x') to be optional,
        or without any (just 'x') for a positional argument;
        For optional parameter, 'name' will be interpreted as an argument name with '--' for argparse
        and without - for function call. You may also define a short-name (or full-name) in args like '-x' (single dash);
        if not provided, full form will be used for short one and vice versa.
        """

        if name[0] != '-':
            bare_name = name
        else:
            bare_name = name[2:] if name[:2] == '--' else name[1:]
            short_name = '-' + bare_name
            full_name = '--' + bare_name

            args = [short_name, full_name] + list(args)     # if other names are given, they'll overwrite these

        self.arguments[bare_name] = [[name] + list(args), kwargs]
        return self

    def set_func(self, f):
        """provide a function to call when command is entered; signature must fit declared parameters; Example:
        c = QRCommand('cmd')
        c.add_argument('a', type=str)
        c.add_argument('b', type=int)
        def f(a: str, b: int):
            return True
        c.set_func(f)
        """
        self.func = f
        return self


class QRConsole:
    """Provides in-process console with configurable commands, their arguments and documentation based on argparse lib.
    Usage example:
        console = QRConsole(hello='hello')
        console.add_command(QRCommand('add', lambda a, b: print(a + b), 'sum 2 integers')
                            .add_argument('a', type=int, help='1st arg')
                            .add_argument('b', type=int, help='2nd arg'))
        console.add_command(QRCommand('sub', lambda a, b: print(a - b), 'differ 2 integers')
                            .add_argument('-a', type=int, default=0, help='1st arg')
                            .add_argument('--value', '-v', type=int, help='2nd arg'))
        console.add_command(QRCommand('one', lambda v, i: print(v + 1 if i else v - 1), 'change value by 1')
                            .add_argument('v', type=int)
                            .add_argument('-i', '--flag', action='store_true', help='set to inc; default is dec')
                            )
        console.run()
    """

    def __init__(self, hello=None, throw_errors: bool = False):
        self.parser = ThrowingArgumentParser(prog='PROG')
        self.subparsers = self.parser.add_subparsers()
        self.commands = []

        self.hello = hello
        self.__print_hello()
        self.throw_errors = throw_errors

    def run(self):
        while True:
            self.__read_line()

    def add_command(self, cmd: QRCommand):
        if cmd.func is None:
            raise Exception(f'command \'{cmd.name}\' has no function set!')

        parser = self.subparsers.add_parser(name=cmd.name, prog=cmd.name, help=cmd.help)
        for args, kwargs in cmd.arguments.values():
            parser.add_argument(*args, **kwargs)

        def extract_args(data):
            return [data.__dict__[arg] for arg in cmd.arguments.keys()]

        parser.set_defaults(func=lambda data: cmd.func(*extract_args(data)))

        self.commands.append(cmd)

    def __print_hello(self):
        if self.hello:
            print(self.hello)
        print("Type '-h' or '--help' to get more info")
        print("Enter commands:")

    def __read_line(self):
        is_help = None
        try:
            s = self.extract_args(input('?>'))
            is_help = ('-h' in s) or ('--help' in s)
            args = self.parser.parse_args(s)
            if args.__contains__('func') and not is_help:
                args.func(args)
        except Exception as ex:
            if not is_help:
                print(Fore.RED + str(ex))
                print(Style.RESET_ALL, end='')
                if self.throw_errors:
                    sys.exit(1)

    def extract_args(self, s):
        p = r'\"([A-Za-z0-9а-яА-Я_ -]+)\"'
        b_args = ['"' + x + '"' for x in re.findall(p, s)]
        fill = f'$^$$^$'
        for i in range(len(b_args)):
            s = s.replace(b_args[i], fill)

        args = s.split()
        i = 0
        for j in range(len(args)):
            if args[j] == fill:
                args[j] = b_args[i][1:-1]
                i += 1
        return args


if __name__ == '__main__':
    console = QRConsole(hello='hello')
    console.add_command(QRCommand('add', lambda a, b: print(a + b), 'sum 2 integers')
                        .add_argument('a', type=int, help='1st arg')
                        .add_argument('b', type=int, help='2nd arg'))
    console.add_command(QRCommand('sub', lambda a, b: print(a - b), 'differ 2 integers')
                        .add_argument('-a', type=int, default=0, help='1st arg')
                        .add_argument('--value', '-v', type=int, help='2nd arg'))
    console.add_command(QRCommand('one', lambda v, i: print(v + 1 if i else v - 1), 'change value by 1')
                        .add_argument('v', type=int)
                        .add_argument('-i', '--flag', action='store_true', help='set to inc; default is dec')
                        )
    console.run()
