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

class UserError(Exception):
    pass

class ConflictDetector:
    def __init__(self, error_msg):
        self._error_msg = error_msg
        self._is_conflict = False
    
    def __call__(self):
        if self._is_conflict:
            raise UserError(self._error_msg)
        else:
            self._is_conflict = True

def read_list(path):
    l = []
    
    with open(path, encoding='utf-8', newline='\n') as fd:
        for item in filter(None, map(lambda s: s.strip(), fd)):
            if item not in l:
                l.append(item)
    
    return l

def cat(result, l):
    for item in l:
        if item not in result:
            result.append(item)

def sub(result, l):
    for item in l:
        if item in result:
            result.remove(item)

def write_result(result, out=None):
    if out is not None:
        with open(out, mode='w', encoding='utf-8', newline='\n') as fd:
            for item in result:
                fd.write('{}\n'.format(item))
    else:
        for item in result:
            print(item)

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
    
    order_confl_det = ConflictDetector('Order conflict')
    result = []
    
    for path in args.cat:
        l = read_list(path)
        cat(result, l)
    
    if args.sub is not None:
        for path in args.sub:
            l = read_list(path)
            sub(result, l)
    
    if args.use_sort:
        order_confl_det()
        result.sort()
    
    if args.use_random:
        order_confl_det()
        
        from random import shuffle
        
        shuffle(result)
    
    write_result(result, out=args.out)
