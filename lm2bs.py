#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os.path
import argparse
import json
import lxml.etree as ET

parser = argparse.ArgumentParser(description='Convert LooksMenu slider preset json to Bodyslide xml')
parser.add_argument('JSONFILE', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('--name', '-n', default='LooksMenu Import')
parser.add_argument('--set', '-s', default='CBBE Body')
parser.add_argument('--group', '-g', default='CBBE')

def main():
    try:
        convert_file()
    except KeyboardInterrupt:
        sys.exit(1)
 
def convert_file():
    """ Read SetSlider values from SliderPreset/Preset and create the corresponding json """
    args = parser.parse_args()
    doc = json.load(args.JSONFILE)

    root = ET.Element('SliderPresets')

    preset = ET.SubElement(root, 'Preset')
    preset.set('name', args.name)
    preset.set('set', args.set)
    group = ET.SubElement(preset, 'Group')
    group.set('name', args.group)

    for slider, value in doc['BodyMorphs'].items():
        setslider = ET.SubElement(preset, 'SetSlider')
        setslider.set('name', slider)
        setslider.set('size', 'big')
        setslider.set('value', str(int(value * 100)))

    print('<?xml version="1.0" encoding="UTF-8"?>')
    print(ET.tostring(root, pretty_print=True,encoding='unicode'))

if __name__ == "__main__":
    main()