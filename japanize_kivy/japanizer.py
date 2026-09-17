#!/usr/bin/env python

import os
import pathlib
import sys

from kivy.core.text import DEFAULT_FONT
from kivy.core.text import LabelBase
from kivy.logger import Logger
from kivy.resources import resource_add_path

RESOURCE_PATH = pathlib.Path(__file__).parent / "resources/ipaexg00401"

# 同梱している IPAex ゴシックのパス
BUNDLED_FONT_PATH = RESOURCE_PATH / "ipaexg.ttf"

# 同梱しているフォントを常に引ける別名
BUNDLED_FONT_NAME = "ipaexg"

# 使用するフォントを指定する環境変数
FONT_ENVVAR = "JAPANIZE_KIVY_FONT"


def _resolve(font):
    """フォントの指定をファイルのパスに解決する

    ファイルとして解決できないときは Kivy のリソースパスからの解決に任せる
    """
    path = pathlib.Path(font).expanduser()
    if path.is_file():
        return str(path)
    return str(font)


def _font_from_environ():
    """環境変数で指定されたフォントを取得する

    指定がない、あるいは指定が不正なときは None を返す
    """
    font = os.environ.get(FONT_ENVVAR)
    if not font:
        return None

    path = pathlib.Path(font).expanduser()
    if not path.is_file():
        Logger.warning(f"Japanize: {FONT_ENVVAR} のフォントが見つからないため同梱のフォントを使う: {font}")
        return None

    return path


def japanize(font=None, *, italic=None, bold=None, bold_italic=None, name=None):
    """日本語を表示できるフォントを Kivy に登録する

    :param font: 使用するフォントファイルのパス。
                 省略すると環境変数 JAPANIZE_KIVY_FONT、それもなければ同梱の IPAex ゴシックを使う
    :param italic: 斜体に使うフォントファイルのパス。省略すると font と同じものを使う
    :param bold: 太字に使うフォントファイルのパス。省略すると font と同じものを使う
    :param bold_italic: 太字かつ斜体に使うフォントファイルのパス。省略すると font と同じものを使う
    :param name: 登録する名前。省略すると Kivy の既定のフォント名になり、アプリケーション全体に適用される
    :return: 登録した名前
    :raises OSError: 指定されたフォントファイルが見つからないとき
    """
    # 同梱しているフォントは、別のフォントに差し替えても使えるようにしておく
    resource_add_path(str(RESOURCE_PATH))
    LabelBase.register(BUNDLED_FONT_NAME, str(BUNDLED_FONT_PATH))

    if font is None:
        font = _font_from_environ() or BUNDLED_FONT_PATH

    if name is None:
        name = DEFAULT_FONT

    # 指定のないスタイルには Kivy が font と同じものを使う
    styles = [_resolve(style) if style is not None else None for style in (italic, bold, bold_italic)]
    LabelBase.register(name, _resolve(font), *styles)

    return name


def show_license():
    license_agreement_filepath = RESOURCE_PATH / "IPA_Font_License_Agreement_v1.0.txt"
    # ファイルは BOM 付きの UTF-8 になっている
    license_agreement = license_agreement_filepath.read_text(encoding="utf-8-sig")
    print(license_agreement, file=sys.stderr)  # ruff: ignore[print]
