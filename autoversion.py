#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'jtullos'
__version__ = '1.16.54'

# The MIT License (MIT)
# Copyright (c) 2016 John Andrew Tullos (xeek@xeekworx.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this 
# software and associated documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to the following 
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies 
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import argparse
import platform
from datetime import *

VERSION = __version__
DEFAULT_NAME = 'autoversion'


def main(argv = None):

    # HANDLE COMMAND-LINE ARGUMENTS:
    if not argv:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description = DEFAULT_NAME, 
                                     add_help = False)
    parser.add_argument('source',
                        metavar='FILE', 
                        type=str, 
                        nargs=1,
                        help='Source file to modify')
    parser.add_argument('macros',
                        metavar='MACRO', 
                        type=str, 
                        nargs='*', 
                        help='Macros to modify')
    parser.add_argument('--pyversion', required=False,
                        action='store_true',
                        help='Display Python version')
    parser.add_argument('--version', '-v', required=False,
                        action='store_true',
                        help='Display Python version')
    parser.add_argument('--help', '-?', action='help')
    try:
        args = parser.parse_args(argv)
        if len(args.macros) < 1:
            parser.print_usage()
            print('At least one macro argument is required.')
            raise
    except:
        return 1

    # DISPLAY AUTOVERSION VERSION:
    if args.version:
        print("Autoversion Version %s" % __version__)

    # DISPLAY PYTHON VERSION:
    if args.pyversion:
        print("Python Version %s" % platform.python_version())
    
    # FILE PARSING
    try:
        file = open(args.source[0], "r+")
        source = file.readlines()
    except exception as e:
        print('Failed to open file. ' + e.msg)
        return 1

    # C++ MACRO PARSING:
    line_number = 1
    new_source = ""
    for line in source:
        if not line.strip().startswith('#define'):
            new_source += line
        else:
            values = line.split(None, 3) # value[0] = #define, value[1] = macro name, value[2] = data to modify
            if len(values) > 2 and values[1] in args.macros:
                # Remove any quotes and trailing \0 if they exist:
                macro_value = values[2].strip('"').replace('\\0', '')
                # Determine the seperator being used:
                separator = '.'
                for c in macro_value:
                    if not c.isdigit():
                        separator = c
                # Get value parts:
                parts = macro_value.split(separator, 4)
                # [0] Major:    This is usually left alone and changed manually by the developer,
                #               unless it's the only part in the version; then it's incremented.
                if len(parts) == 1:
                    parts[0] = str(int(parts[0]) + 1)
                # [1] Minor:    This is the last 2 digits of the current year.
                if len(parts) > 1:
                    parts[1] = datetime.now().strftime('%y')
                # [2] Revision: This is the digits for the month combined with the digits for the day.
                if len(parts) > 2:
                    parts[2] = datetime.now().strftime('%m').strip('0') + datetime.now().strftime('%d').strip('0')
                # [3] Build:    This is just simply incremented + 1.
                if len(parts) > 3:
                    parts[3] = str(int(parts[3]) + 1)
                # Update:
                modified_macro_value = separator.join(parts)
                modified_line = line.replace(macro_value, modified_macro_value)
                new_source += modified_line

                print("Line %d: Updated %s from '%s' to '%s'" % (line_number, values[1], macro_value, modified_macro_value))
            else:
                new_source += line
        line_number += 1
                
    # WRITE THE NEW SOURCE TO THE FILE & CLOSE:    
    file.seek(0)
    file.write(new_source)
    file.truncate()
    file.close()

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        pass
    
