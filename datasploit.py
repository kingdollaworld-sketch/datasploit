#!/usr/bin/env python

import re
import sys
import shutil
import os
import textwrap
import argparse

try:
    from core import TargetType, classify_target, get_runner, is_private_ip
except ModuleNotFoundError:  # Imported as part of the datasploit package
    from .core import TargetType, classify_target, get_runner, is_private_ip


def main():
    output=None
    desc = r"""
   ____/ /____ _ / /_ ____ _ _____ ____   / /____   (_)/ /_
  / __  // __ `// __// __ `// ___// __ \ / // __ \ / // __/
 / /_/ // /_/ // /_ / /_/ /(__  )/ /_/ // // /_/ // // /_
 \__,_/ \__,_/ \__/ \__,_//____// .___//_/ \____//_/ \__/
                               /_/

            Open Source Assistant for #OSINT
                www.datasploit.info

    """
    desc = desc.replace("\\\\", "\\")
    epilog="""              Connect at Social Media: @datasploit
                """
    # Banner print
    print(textwrap.dedent(desc))
    print(textwrap.dedent(epilog))
    # Set all parser arguments here.
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent(desc),epilog=epilog)
    parser.add_argument("-i","--input",help="Provide Input",dest='single_target')
    parser.add_argument("-f","--file",help="Provide Input",dest='file_target')
    parser.add_argument("-a","--active",help="Run Active Scan attacks",dest='active',action="store_false")
    parser.add_argument("-q","--quiet",help="Run scans in automated manner accepting default answers",dest='quiet',action="store_false")
    parser.add_argument("-o","--output",help="Provide Destination Directory",dest='output')
    # check and ensure the config file is present otherwise create one. required for all further operations
    ds_dir=os.path.dirname(os.path.realpath(__file__))
    config_candidates = ["config.ini", "config.py"]
    config_paths = [os.path.join(ds_dir, name) for name in config_candidates]
    config_template_candidates = [
        os.path.join(ds_dir, "config.template.ini"),
        os.path.join(ds_dir, "config_sample.py"),  # Legacy name
    ]

    config_file_path = next((path for path in config_paths if os.path.exists(path)), None)
    if config_file_path is None:
        print("[+] Looks like a new setup, setting up the config file.")
        template_path = next((path for path in config_template_candidates if os.path.exists(path)), None)
        if not template_path:
            raise FileNotFoundError("No configuration template found. Expected config.template.ini.")

        config_file_path = os.path.join(ds_dir, "config.ini")
        shutil.copyfile(template_path, config_file_path)
        print("[+] A config file is added please follow guide at https://datasploit.github.io/datasploit/apiGeneration/ to fill API Keys for better results")
        # We can think about quiting at this point.
    # parse arguments in case they are provided.
    x=parser.parse_args()
    active=x.active
    quiet=x.quiet
    single_input=x.single_target
    file_input=x.file_target
    output=x.output
    # if no target is provided print(help and quit.)
    if not (single_input or file_input):
        print("\nSingle target or file input required to run\n")
        parser.print_help()
        sys.exit()
    if single_input:
        try:
            auto_select_target(single_input, output)
        except KeyboardInterrupt:
            print("\nCtrl+C called Quiting")
    if file_input:
        try:
            if os.path.isfile(file_input):
                print("File Input: %s" % file_input)
                with open(file_input, 'r') as f:
                    for target in f:
                        auto_select_target(target.rstrip(), output)
                print("\nDone processing %s" % file_input)
            else:
                print("%s is not a readable file" % file_input)
                print("Exiting...")
        except KeyboardInterrupt:
            print("\nCtrl+C called Quiting")

def auto_select_target(target, output=None):
    """Determine the target type and execute the relevant collectors."""
    print("Target: %s" % target)

    if is_private_ip(target):
        print("Internal IP detected. Skipping target.")
        return

    target_type = classify_target(target)
    messages = {
        TargetType.IP: "Looks like an IP, running IP collectors...",
        TargetType.DOMAIN: "Looks like a DOMAIN, running domain collectors...",
        TargetType.EMAIL: "Looks like an EMAIL, running email collectors...",
        TargetType.USERNAME: "Nothing matched; treating input as USERNAME...",
    }
    print(messages[target_type] + "\n")

    runner = get_runner()
    runner.run(target_type, target, output)

if __name__ == "__main__":
   main()
