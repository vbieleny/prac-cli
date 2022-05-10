#!/usr/bin/env python3

import subprocess
import shutil
import argparse
import os
import sys
import pathlib

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PRAC CLI utility.')
    parser.add_argument('command', type=str, nargs='+', help='specific command, such as "create" or "run" and subsequent subcommands')
    parser.add_argument('-v', '--verbose', action='store_true', help='will output debug information to standard output')
    args = parser.parse_args()
    pracpath = pathlib.Path.home() / '.prac' / 'core'

    makepath = shutil.which('make')
    cwd = pathlib.Path(os.getcwd())
    pracdir = cwd / '.prac'

    if args:
        if not (cwd / 'prac.ini').is_file() and args.command[0] != 'create':
            sys.exit('You are not in a project directory.')

        if args.command[0] == 'create':
            commandargs = [makepath, '-C', pracpath, 'template', f'TEMPLATEDIR={cwd.resolve()}']
            if not args.verbose:
                commandargs.append('-s')
            returncode = subprocess.call(commandargs)
            if returncode != 0:
                sys.exit('Creatng project failed!')
            print('Project created successfully.')
        elif args.command[0] == 'build':
            commandargs = [makepath, '-C', pracdir.resolve(), 'all']
            if not args.verbose:
                commandargs.append('-s')
            returncode = subprocess.call(commandargs)
            if returncode != 0:
                sys.exit('Building project failed!')
            print('Project built successfully.')
        elif args.command[0] == 'clean':
            commandargs = [makepath, '-C', pracdir.resolve(), 'clean']
            if not args.verbose:
                commandargs.append('-s')
            returncode = subprocess.call(commandargs)
            if returncode != 0:
                sys.exit('Cleaning project failed!')
            print('Project cleaned successfully.')
        elif args.command[0] == 'run':
            commandargs = [makepath, '-C', pracdir.resolve(), 'qemu-serial']
            if not args.verbose:
                commandargs.append('-s')
            returncode = subprocess.call(commandargs)
            if returncode != 0:
                sys.exit('Running project failed!')
