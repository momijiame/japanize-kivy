#!/usr/bin/env python
# -*- coding: utf-8 -*-

import builtins

from setuptools import setup


def main():
    # XXX: setup process detection hack
    builtins.__JAPANIZE_KIVY_SETUP__ = True

    setup()


if __name__ == '__main__':
    main()
