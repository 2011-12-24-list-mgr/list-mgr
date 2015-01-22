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
import re

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

def run_filter_func_list(filter_func_list, item):
    assert isinstance(item, str) and item
    
    for filter_func in filter_func_list:
        item = filter_func(re=re, item=item)
        
        if not item:
            break
        
        if not isinstance(item, str):
            item = str(item)
        item = item.strip()
        
        if not item:
            break
    
    return item

def read_list(path, filter_func_list):
    l = []
    
    with open(path, encoding='utf-8', errors='replace') as fd:
        for item in filter(None, map(lambda s: s.strip(), fd)):
            item = run_filter_func_list(filter_func_list, item)
            
            if not item:
                continue
            
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

def write_result(result, out, filter_func_list):
    def filtered_result():
        for item in result:
            item = run_filter_func_list(filter_func_list, item)
            
            if not item:
                continue
            
            yield item
    
    if out is not None:
        with open(out, mode='w', encoding='utf-8', newline='\n') as fd:
            for item in filtered_result():
                fd.write('{}\n'.format(item))
    else:
        for item in filtered_result():
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
            '--cat-filter-py-expr',
            metavar='PYTHON-EXPR',
            action='append',
            help='using filter (expression string in Python Language) after concatenation input. '
                    'example: "item if item.isupper() else None". '
                    'yet example: "item if re.match(r\'^foo\', item) else None"',
            )
    
    parser.add_argument(
            '--sub-filter-py-expr',
            metavar='PYTHON-EXPR',
            action='append',
            help='using filter (expression string in Python Language) after substraction input. '
                    'see examples for argument --cat-filter-py-expr',
            )
    
    parser.add_argument(
            '--out-filter-py-expr',
            metavar='PYTHON-EXPR',
            action='append',
            help='using filter (expression string in Python Language) before output. '
                    'example: "item.upper()". '
                    'see other examples for argument --cat-filter-py-expr',
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
    
    cat_filter_func_list = []
    if args.cat_filter_py_expr is not None:
        for py_expr in args.cat_filter_py_expr:
            filter_code = compile(py_expr, '<cat_filter_py_expr>', 'eval')
            def filter_func(_filter_code=filter_code, **kwargs):
                return eval(_filter_code, kwargs)
            cat_filter_func_list.append(filter_func)
    
    sub_filter_func_list = []
    if args.sub_filter_py_expr is not None:
        for py_expr in args.sub_filter_py_expr:
            filter_code = compile(py_expr, '<sub_filter_py_expr>', 'eval')
            def filter_func(_filter_code=filter_code, **kwargs):
                return eval(_filter_code, kwargs)
            sub_filter_func_list.append(filter_func)
    
    out_filter_func_list = []
    if args.out_filter_py_expr is not None:
        for py_expr in args.out_filter_py_expr:
            filter_code = compile(py_expr, '<out_filter_py_expr>', 'eval')
            def filter_func(_filter_code=filter_code, **kwargs):
                return eval(_filter_code, kwargs)
            out_filter_func_list.append(filter_func)
    
    for path in args.cat:
        l = read_list(path, cat_filter_func_list)
        cat(result, l)
    
    if args.sub is not None:
        for path in args.sub:
            l = read_list(path, sub_filter_func_list)
            sub(result, l)
    
    if args.use_sort:
        order_confl_det()
        result.sort()
    
    if args.use_random:
        order_confl_det()
        
        from random import shuffle
        
        shuffle(result)
    
    write_result(result, args.out, out_filter_func_list)
