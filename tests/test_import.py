#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


def test_import():
    """test to import with no error"""
    import japanize_kivy


if __name__ == '__main__':
    pytest.main(['-v', __file__])
