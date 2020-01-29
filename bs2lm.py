#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os.path
import argparse
import json
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Convert BodySlide xml preset to LooksMenu json')
parser.add_argument('XMLFILE', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('-w', '--weight', action='store_true', help='Add centered weight triangle to output json')

def main():
    try:
        convert_file()
    except KeyboardInterrupt:
        sys.exit(1)

def convert_file():
    """ Read Bodytalk xml and baseline offset files and print result as json """
    args = parser.parse_args()
    tree = ET.parse(args.XMLFILE)
    root = tree.getroot()

    doc = {}
    doc.update({"BodyMorphs": {}})

    for slider in root.iter('SetSlider'):
        doc['BodyMorphs'].update({slider.get('name') : int(slider.get('value'))/100})

    if args.weight:
        doc.update({"Weight" : [1/3, 1/3, 1/3]})

    print(json.dumps(doc, indent=4))

if __name__ == "__main__":
    main()
