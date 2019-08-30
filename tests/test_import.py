#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

import japanize_kivy


def test_show_license():
    """test to show license"""
    japanize_kivy.show_license()


if __name__ == '__main__':
    pytest.main(['-v', __file__])
