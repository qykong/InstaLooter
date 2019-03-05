#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Running a test example.
"""

import sys
from instalooter.cli import main


def usage():
    return '''
        python run_example.py user chuuu_0908 ./output -t 2018-12-31:2018-01-01 -n 25 -D -e --traceback -N
    '''


if __name__ == '__main__':
    main()
    # is the same as
    # main(sys.argv[1:])
