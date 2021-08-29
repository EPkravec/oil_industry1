#!/usr/bin/python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    import argparse
    import os, re

    def increment_line(args):
        """
        Ф-я выведения версии библиотеки с ее последующей записью в файл setup.py в библиотеке
        return: производит запись версии в файл etup.py в библиотеки
        """
        vi = [int(i) for i in __version__.split('.')]

        if len(vi) == 3:
            vi.append(0)
        if args.M:
            vi[0] += 1
            vi[1] = 0
            vi[2] = 0
            vi[3] = 0
        elif args.m:
            vi[1] += 1
            vi[2] = 0
            vi[3] = 0
        elif args.p:
            vi[2] += 1
            vi[3] = 0
        elif args.b:
            vi[3] += 1
        vs = [str(i) for i in vi]
        nv = '.'.join(vs)
        print('new version: %s' % nv)
        return '__version__ = "%s"\n' % nv

    setup = os.path.dirname(os.path.abspath(__file__)) + '/setup.py'

    with open(setup, 'r') as f:
        lines = f.readlines()

    for lno in range(len(lines)):
        x = re.search(ur'^\s*__version__\s*=\s*"(.*)"\s*$', lines[lno])
        if x:
            __version__ = x.group(1)
            break

    print('current version: %s' % __version__)

    parser = argparse.ArgumentParser()
    parser.add_argument("-M", action='store_true', help="increment major X.0.0.0")
    parser.add_argument("-m", action='store_true', help="increment minor 0.X.0.0")
    parser.add_argument("-p", action='store_true', help="increment patch 0.0.X.0")
    parser.add_argument("-b", action='store_true', help="increment build 0.0.0.X")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        exit()

    lines[lno] = increment_line(args)

    with open(setup, 'w') as f:
        f.write(''.join(lines))
