#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pathlib

from kivy.resources import resource_add_path
from kivy.core.text import LabelBase
from kivy.core.text import DEFAULT_FONT


RESOURCE_PATH = pathlib.Path(__file__).parent / 'resources/ipaexg00401'


def japanize():
    resource_add_path(str(RESOURCE_PATH))
    LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')


def show_license():
    license_agreement_filepath = RESOURCE_PATH / 'IPA_Font_License_Agreement_v1.0.txt'
    with open(str(license_agreement_filepath), mode='r') as fp:
        print(fp.read(), file=sys.stderr)
