#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess
import zipfile
import logging
from types import SimpleNamespace
from datetime import datetime

"""
Limitations:
    * Can only update code to existing functions
    * Cannot create new functions
    * Does not provide means to edit lambda configuration settings (i.e function handler name)
    * Will not work for project structures bundled in to the lambda zip
"""

# TODO: Test what happens when zipfile executes zip to existing path. Does the zip just get updated?
# TODO: Paramaterize the build dir via CLI flag
# TODO: Add single letter flag variants
# TODO: Write tests


BUILD_DIR = "./build"


def err(msg):
    """
    : Add basic boilerplate around error message.
    """
    return f"Error: {msg}. See `--help` for more information."


def init_logger(log_level="DEBUG", stream=sys.stdout):
    """
    : Init the logger.
    """
    log_level_int = getattr(logging, log_level, None)
    if log_level_int == None:
        logging.warn(
            "Obtained unrecognized log_level`{log_level}`. Reverting to 'INFO'"
        )
        log_level_int = getattr(logging, "INFO")
    log = logging.getLogger()
    log.setLevel(log_level_int)
    handler = logging.StreamHandler(stream)
    handler.setLevel(log_level)
    log.addHandler(handler)
    return log


def get_file_info(path):
    """
    : Get basic file information from a file path.
    """
    source = path
    exists = os.path.exists(path)
    isfile = os.path.isfile(path)
    isdir = os.path.isdir(path)
    abspath = os.path.abspath(path)
    root, leaf = os.path.split(abspath)
    leaf_name = leaf
    extension = None
    if isfile:
        leaf_name, extension = os.path.splitext(leaf)
    obj = SimpleNamespace(
        source=source,
        exists=exists,
        isfile=isfile,
        isdir=isdir,
        abspath=abspath,
        root=root,
        leaf=leaf,
        leaf_name=leaf_name,
        extension=extension,
    )
    return obj


def get_args():
    """
    : Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Publish a python module to AWS as a Lambda function"
    )
    parser.add_argument(
        "fname", type=str, metavar="FNAME", help="The AWS lambda function name."
    )
    parser.add_argument(
        "module", type=str, metavar="MODULE", help="The python module path to upload."
    )
    parser.add_argument(
        "--dry-run",
        default=False,
        action="store_true",
        help="Run script, but dont poste zip bundle to AWS.",
    )
    parser.add_argument(
        "--log",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        dest="log_level",
        help="Set logging level.",
    )
    return parser.parse_args()


def main():
    # parse CLI args
    args = get_args()

    # setup logging
    log = init_logger(args.log_level)

    # Get module file info
    log.debug(f"Command Line Args: {args}")
    file_info = get_file_info(args.module)
    log.debug(f"Module info: {file_info}")

    # validate module
    if not file_info.exists:
        sys.exit(err(f"Python module argument `{args.module}` does not exist"))
    if file_info.isdir or not file_info.isfile:
        sys.exit(err(f"Python module argument `{args.module}` is not a file"))
    if file_info.extension != ".py":
        sys.exit(err(f"Python module argument `{args.module}` is not a `.py` file"))

    # compress module to .zip file
    zip_path = os.path.join(BUILD_DIR, file_info.leaf_name + ".zip")
    with zipfile.ZipFile(zip_path, "w") as zf:
        # NOTE: This is using arcname to remove any uneeded parent directories; however,
        # for a module with imports/dependancies this wont work
        zf.write(file_info.abspath, arcname=file_info.leaf)

    # Run subprocess call to AWS cli
    zip_file_info = get_file_info(zip_path)
    logging.debug(f"Zip file info: {zip_file_info}")
    zip_path = "fileb://" + zip_file_info.abspath
    cmd = [
        "aws",
        "lambda",
        "update-function-code",
        "--function-name",
        args.fname,
        "--zip-file",
        zip_path,
    ]
    log.debug(f"AWS subprocess command: `{' '.join(cmd)}`")

    if not args.dry_run:
        subprocess.run(cmd)


if __name__ == "__main__":
    main()
