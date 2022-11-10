# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2022-11-10 16:43:04
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2022-11-10 16:50:59
@FilePath: \thefuck\main.py
@Description:
'''
# Initialize output before importing any module, that can use colorama.
from thefuck.system import init_output

init_output()

import os  # noqa: E402
import sys  # noqa: E402
from thefuck import logs  # noqa: E402
from thefuck.argument_parser import Parser  # noqa: E402
from thefuck.utils import get_installation_version  # noqa: E402
from thefuck.shells import shell  # noqa: E402
from thefuck.entrypoints.alias import print_alias  # noqa: E402
from thefuck.entrypoints.fix_command import fix_command  # noqa: E402


def main():
    parser = Parser()
    known_args = parser.parse(sys.argv)

    if known_args.help:
        parser.print_help()
    elif known_args.version:
        logs.version(get_installation_version(),
                     sys.version.split()[0], shell.info())
    # It's important to check if an alias is being requested before checking if
    # `TF_HISTORY` is in `os.environ`, otherwise it might mess with subshells.
    # Check https://github.com/nvbn/thefuck/issues/921 for reference
    elif known_args.alias:
        print_alias(known_args)
    elif known_args.command or 'TF_HISTORY' in os.environ:
        fix_command(known_args)
    elif known_args.shell_logger:
        try:
            from thefuck.entrypoints.shell_logger import shell_logger  # noqa: E402
        except ImportError:
            logs.warn('Shell logger supports only Linux and macOS')
        else:
            shell_logger(known_args.shell_logger)
    else:
        parser.print_usage()

sys.exit(main())