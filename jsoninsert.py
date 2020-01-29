#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os.path
import argparse
import json

parser = argparse.ArgumentParser(description='Overwrites json entries in FILE1 with entries from FILE2')
parser.add_argument('FILE1', type=argparse.FileType('r'))
parser.add_argument('FILE2', type=argparse.FileType('r'))
parser.add_argument('-t', '--tags', nargs='+', default=['BodyMorphs'], type=str)
parser.add_argument('-c', '--clear', action='store_true', 
                    help='Clear all TAGS entries from FILE1 before inserting.')
parser.add_argument('-a', '--add', action='store_true',
                    help='Add the values in FILE1 and FILE2 if both exist.')
parser.add_argument('-s', '--subtract', action='store_true',
                    help='Subtract the values in FILE2 from FILE1.')


def main():
    try:
        process_files()
    except KeyboardInterrupt:
        sys.exit(1)

def process_files():
    """ Read files, insert data from FILE2 to FILE1 and print output """
    args = parser.parse_args()
    doc1 = json.load(args.FILE1)
    doc2 = json.load(args.FILE2)

    for tag in args.tags:
        if tag not in doc2:
            continue
    
        if isinstance(doc2[tag], list):
            """ For lists, just overwrite list data """
            doc1.update({ tag : doc2[tag]})
        else:
            if args.clear or tag not in doc1:
                """ Clearing the element results in only elements from FILE2 in output """
                doc1[tag] = {}

            """ If add or subtract, calculate result first in doc2 """
            if args.add or args.subtract:
                for element, value in doc2[tag].items():
                    if args.subtract:
                        doc2[tag][element] = -doc2[tag][element]
                    try:
                        doc2[tag][element] += doc1[tag][element]
                    except KeyError:
                        pass

            """ Overwrite all elements """
            for element, value in doc2[tag].items():
                doc1[tag].update({element : value})

    print(json.dumps(doc1, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
