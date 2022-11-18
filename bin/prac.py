#!/usr/bin/env python3

import subprocess
import shutil
import argparse
import os
import sys
import pathlib
import urllib.request
import zipfile
import tarfile

toolchain_download_link = 'https://github.com/vbieleny/gcc-i686-elf-toolchain/releases/download/v11.3.0/gcc-i686-elf-toolchain.tar.xz'
core_download_link = 'https://github.com/vbieleny/page-algorithm-comparison/archive/refs/heads/develop.zip'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PRAC CLI utility.')
    parser.add_argument('command', type=str, nargs='+', help='specific command, such as "create" or "run" and subsequent subcommands')
    parser.add_argument('-v', '--verbose', action='store_true', help='will output debug information to standard output')
    args = parser.parse_args()
    pracpath = pathlib.Path.home() / '.prac'
    corepath = pracpath / 'core'
    toolchainpath = pracpath / 'gcc-i686-elf-toolchain'

    makepath = shutil.which('make')
    cwd = pathlib.Path(os.getcwd())
    newpracdir = cwd / '.prac'

    if args:
        if args.command[0] == 'init':
            if toolchainpath.is_dir() and corepath.is_dir():
                print(f'PRAC is already initialized. If you want to reinitialize it, delete "{pracpath.resolve()}" directory')
                sys.exit()

            if not pracpath.is_dir():
                pracpath.mkdir(parents=True)

            if not toolchainpath.is_dir():
                toolchaintar = (pracpath / 'gcc-i686-elf-toolchain.tar.xz').resolve()
                if not toolchaintar.is_file():
                    print('Downloading x86 toolchain...')
                    urllib.request.urlretrieve(toolchain_download_link, toolchaintar)
                dirname = ''
                with tarfile.open(toolchaintar, 'r') as toolchaintar:
                    dirname = toolchaintar.getnames()[0]
                    print('Extracting x86 toolchain...')
                    def is_within_directory(directory, target):
                        
                        abs_directory = os.path.abspath(directory)
                        abs_target = os.path.abspath(target)
                    
                        prefix = os.path.commonprefix([abs_directory, abs_target])
                        
                        return prefix == abs_directory
                    
                    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                    
                        for member in tar.getmembers():
                            member_path = os.path.join(path, member.name)
                            if not is_within_directory(path, member_path):
                                raise Exception("Attempted Path Traversal in Tar File")
                    
                        tar.extractall(path, members, numeric_owner=numeric_owner) 
                        
                    
                    safe_extract(toolchaintar, pracpath)
                (pracpath / dirname).rename(toolchainpath)
                (pracpath / 'gcc-i686-elf-toolchain.tar.xz').unlink(missing_ok=True)

            if not corepath.is_dir():
                corezip = (pracpath / 'core.zip').resolve()
                if not corezip.is_file():
                    print('Downloading PRAC core...')
                    urllib.request.urlretrieve(core_download_link, corezip)
                dirname = ''
                with zipfile.ZipFile(corezip, 'r') as corezip:
                    dirname = corezip.namelist()[0]
                    print('Extracting PRAC core...')
                    corezip.extractall(pracpath)
                (pracpath / dirname).rename(corepath)
                (pracpath / 'core.zip').unlink(missing_ok=True)

            print('PRAC successfully initialized!')
            sys.exit()

        if not (cwd / 'prac.ini').is_file() and args.command[0] != 'create':
            sys.exit('You are not in a project directory.')
        
        if args.command[0] == 'create':
            commandargs = [makepath, '-C', corepath, 'template', f'TEMPLATEDIR={cwd.resolve()}']
            if not args.verbose:
                commandargs.append('-s')
            returncode = subprocess.call(commandargs)
            if returncode != 0:
                sys.exit('Creatng project failed!')
            print('Project created successfully.')
        elif args.command[0] == 'build':
            commandargs = [makepath, '-C', newpracdir.resolve(), 'all']
            if not args.verbose:
                commandargs.append('-s')
            returncode = subprocess.call(commandargs)
            if returncode != 0:
                sys.exit('Building project failed!')
            print('Project built successfully.')
        elif args.command[0] == 'clean':
            commandargs = [makepath, '-C', newpracdir.resolve(), 'clean']
            if not args.verbose:
                commandargs.append('-s')
            returncode = subprocess.call(commandargs)
            if returncode != 0:
                sys.exit('Cleaning project failed!')
            print('Project cleaned successfully.')
        elif args.command[0] == 'run':
            commandargs = [makepath, '-C', newpracdir.resolve(), 'qemu-serial']
            if not args.verbose:
                commandargs.append('-s')
            returncode = subprocess.call(commandargs)
            if returncode != 0:
                sys.exit('Running project failed!')
