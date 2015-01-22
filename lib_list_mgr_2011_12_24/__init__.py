# -*- mode: python; coding: utf-8 -*-
#
# Copyright (c) 2011, 2012 Andrej Antonov <polymorphm@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
    
    with open(path, encoding='utf-8', errors='replace') as fd:
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
        description='utility for manipulation with lists (text file format)')
    
    parser.add_argument(
        'cat',
        metavar='CAT-PATH',
        nargs='*',
        help='list (file path) for concatenation',
    )
    
    parser.add_argument(
        '--sub',
        metavar='SUB-PATH',
        action='append',
        help='list (file path) for substraction',
    )
    
    parser.add_argument(
        '--use-sort',
        action='store_true',
        help='using sorting for result',
    )
    
    parser.add_argument(
        '--use-random',
        action='store_true',
        help='using randomization for result',
    )
    
    parser.add_argument(
        '--out',
        metavar='OUT-PATH',
        help='file path for writing result list',
    )
    
    args = parser.parse_args()
    
    order_confl_det = ConflictDetector('order conflict')
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
