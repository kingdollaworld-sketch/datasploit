#!/usr/bin/env python

import os
import shutil
import subprocess
import tempfile

CONFIG_CANDIDATES = ("config.ini", "config.py")
TEMPLATE_CANDIDATES = ("config.template.ini", "config_sample.py")


def _resolve_config_path(base_path):
    for filename in CONFIG_CANDIDATES:
        candidate = os.path.join(base_path, filename)
        if os.path.exists(candidate):
            return candidate
    return os.path.join(base_path, CONFIG_CANDIDATES[0])


def _resolve_template_path(base_path):
    for filename in TEMPLATE_CANDIDATES:
        candidate = os.path.join(base_path, filename)
        if os.path.exists(candidate):
            return candidate
    return None


def edit():
    config_path = os.path.dirname(__file__)
    config_file = _resolve_config_path(config_path)
    if not os.path.exists(config_file):
        print("[+] Looks like a new setup, setting up the config file.")
        template_path = _resolve_template_path(config_path)
        if not template_path:
            raise FileNotFoundError("No configuration template found. Expected config.template.ini.")
        shutil.copyfile(template_path, config_file)
    with open(config_file, "r") as fh:
        config = fh.read()
    fd, fname = tempfile.mkstemp()
    try:
        with open(fname, "w") as fh:
            fh.write(config)
    finally:
        os.close(fd)

    cmd = os.environ.get('EDITOR', 'vi') + ' ' + fname
    subprocess.call(cmd, shell=True)

    with open(fname, "r") as f:
        config = f.read().strip()
        with open(config_file, "w") as fh:
            fh.write(config)

    os.unlink(fname)


if __name__ == "__main__":
    edit()
