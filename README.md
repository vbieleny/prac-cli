# PRAC CLI tool

This simple CLI utility allows you to create new projects for framework [PRAC](https://github.com/vbieleny/page-algorithm-comparison), build, clean or run them.

## Dependencies

To execute this CLI tool, you need Python 3, as this CLI utility is completely written in Python.

## Installation

To install this CLI, you need to download the latest release from the [releases page]() and place it somewhere on your disk (for example in `/opt`). Then you need to add this path to environment variable PATH, so you can execute this CLI tool from anywhere. To do so, add this line to your `~/.bashrc`

```shell
export PATH="$PATH:/path/to/prac/cli/bin"
```

so if you placed the downloaded folder to `/opt`, it should look like this:

```shell
export PATH="$PATH:/opt/prac-cli/bin"
```

## Usage

To initialize toolchain needed for compilation and download the framework, run

```shell
prac init
```

You only need to do this once. This will install all necessary tools in `~/.prac` directory.

To create a new project in the current directory, run

```shell
prac create
```

To build the project, run

```shell
prac build
```

To clean compiled files, run

```shell
prac clean
```

To build and run the project, run

```shell
prac run
```

# License
Distributed under the MIT License. See LICENSE.txt for more information.
