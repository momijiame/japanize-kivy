#!/usr/bin/env python

import pathlib
import sys

from kivy.core.text import DEFAULT_FONT
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path

RESOURCE_PATH = pathlib.Path(__file__).parent / "resources/ipaexg00401"


def japanize():
    resource_add_path(str(RESOURCE_PATH))
    LabelBase.register(DEFAULT_FONT, "ipaexg.ttf")


def show_license():
    license_agreement_filepath = RESOURCE_PATH / "IPA_Font_License_Agreement_v1.0.txt"
    # ファイルは BOM 付きの UTF-8 になっている
    license_agreement = license_agreement_filepath.read_text(encoding="utf-8-sig")
    print(license_agreement, file=sys.stderr)  # ruff: ignore[print]
