#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'jtullos'
__version__ = '1.17.815'

# The MIT License (MIT)
# Copyright (c) 2017 John Andrew Tullos (xeek@xeekworx.com)
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
import time
import re

VERSION = __version__
DEFAULT_NAME = 'autoversion'
DEFAULT_DESC = ('{} is a Python command-line tool that looks for '
                'preprocessor definitions in a C/C++ header file and modifies '
                'the value to increment version values, etc.'.format(DEFAULT_NAME.title()))


def main(argv = None):

    # HANDLE COMMAND-LINE ARGUMENTS:
    if not argv:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description = DEFAULT_DESC, 
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
                        help='Version macros to modify')
    parser.add_argument('--bdate_macro',
                        metavar='MACRO',
                        type=str,
                        nargs=1,
                        help='Build date macro')
    parser.add_argument('-c', '--upcopyright', required=False,
                        action='store_true',
                        help='Update the year in copyrights')
    parser.add_argument('-l', '--lastyear', required=False,
                        action='store_true',
                        help='Update only the last year found in copyrights')
    parser.add_argument('-p', '--pyversion', required=False,
                        action='store_true',
                        help='Display Python version')
    parser.add_argument('-v', '--version', required=False,
                        action='store_true',
                        help='Display Autoversion version')
    parser.add_argument('-?', '--help', action='help')
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
            values = line.split(None, 2) # value[0] = #define, value[1] = macro name, value[2] = data to modify
            if len(values) < 3:
                new_source += line
            if args.bdate_macro and values[1] in args.bdate_macro:
                # Remove any quotes and trailing \0 if they exist:
                macro_value = values[2].replace('\\0', '').replace('\n', '').strip('"')
                # Determine modified value / New build date:
                dt = datetime.now()
                new_build_date = int(time.mktime(dt.timetuple()))
                # Update:
                modified_macro_value = str(new_build_date)
                modified_line = line.replace(macro_value, modified_macro_value)
                new_source += modified_line

                print("Line {}: Updated {} from '{}' to '{}'".format(line_number, values[1], macro_value, modified_macro_value))
            elif args.upcopyright and ('copyright' in values[1].lower() or 'copyright' in values[2].lower()):
                macro_value = values[2].replace('\\0', '').replace('\n', '').strip('"')
                # Current year:
                current_year = str(date.today().year)
                # Find all of the detected years in the order found (left-to-right):
                year_list = re.findall(r"[0-9]{4,4}", macro_value)
                # If there aren't any years, we should probably not do anything.
                if not year_list:
                    new_source += line
                    print("Line {}: {} NOT Updated. Copyright had no year in it!".format(line_number, values[1]))
                else:
                    if args.lastyear:
                        # Replace only the last occurance of a year with the current year:
                        yearpos = macro_value.rfind(year_list[-1])
                        modified_macro_value = "{}{}{}".format(
                            macro_value[:yearpos],
                            current_year,
                            macro_value[yearpos+4:]
                            )

                        print("Line {}: Updated {} year from '{}' to '{}'".format(line_number, values[1], macro_value[yearpos:yearpos+4], current_year))
                    else:
                        # Creating a set of all of the years to remove duplicates:
                        year_set = set(year_list)
                        # Replace every found year with the current year:
                        modified_macro_value = macro_value
                        for year in year_set:
                            modified_macro_value = modified_macro_value.replace(year, current_year)

                        print("Line {}: Updated {} year(s) from '{}' to '{}'".format(line_number, values[1], ', '.join(year_set), current_year))

                    # Update:
                    modified_line = line.replace(macro_value, modified_macro_value)
                    new_source += modified_line

            elif len(values) > 2 and values[1] in args.macros:
                # Remove any quotes and trailing \0 if they exist:
                macro_value = values[2].replace('\\0', '').replace('\n', '').strip('"')
                # Determine the seperator being used:
                separator = '.'
                for c in macro_value:
                    if not c.isdigit():
                        separator = c
                        break
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

                print("Line {}: Updated {} from '{}' to '{}'".format(line_number, values[1], macro_value, modified_macro_value))
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
    
