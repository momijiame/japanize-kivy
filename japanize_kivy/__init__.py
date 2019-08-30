# -*- coding: utf-8 -*-

__version__ = '0.1.1'

try:
    __JAPANIZE_KIVY_SETUP__
except NameError:
    __JAPANIZE_KIVY_SETUP__ = False


if not __JAPANIZE_KIVY_SETUP__:
    from japanize_kivy.japanizer import japanize
    from japanize_kivy.japanizer import show_license
    japanize()
