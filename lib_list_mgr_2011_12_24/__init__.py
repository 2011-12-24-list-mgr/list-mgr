#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2011 Andrej A Antonov <polymorphm@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

assert str is not bytes

import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Utility for manipulation with lists (text file format)')
    
    parser.add_argument(
        'cat',
        nargs='*',
        help='List (file path) for concatenation',
    )
    
    parser.add_argument(
        '--sub',
        action='append',
        help='List (file path) for substraction',
    )
    
    parser.add_argument(
        '--use-sort',
        action='store_true',
        help='Using sorting for result',
    )
    
    parser.add_argument(
        '--use-random',
        action='store_true',
        help='Using randomization for result',
    )
    
    parser.add_argument(
        '--out',
        help='File path for writing result list',
    )
    
    args = parser.parse_args()
    
    if args.out is not None:
        out = open(args.out, mode='w', encoding='utf-8', newline='\n')
    else:
        out = None
    
    print(args) # TEST
