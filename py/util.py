import sys
import os
import logging
from types import SimpleNamespace

def err(msg):
    """
    : Add basic boilerplate around error message.
    """
    return f"Error: {msg}. See `--help` for more information."


def init_logger(log_level="DEBUG", stream=sys.stdout):
    """
    : Init a logger instance.
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
