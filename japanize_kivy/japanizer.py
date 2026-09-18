#!/usr/bin/env python

import os
import pathlib
import stat
import sys

from kivy.core.text import DEFAULT_FONT
from kivy.core.text import LabelBase
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

    解決できないときは例外にする。
    Kivy のリソースパスからの解決に任せると、意図しないフォントが黙って使われることがある
    """
    path = pathlib.Path(font).expanduser()
    # 見つからなければ FileNotFoundError になる
    status = path.stat()

    if not stat.S_ISREG(status.st_mode):
        msg = f"font file expected: {font}"
        raise OSError(msg)

    # 相対パスのままだと Kivy のキャッシュによって別のファイルに解決されることがある
    return str(path.resolve())


def _font_from_environ():
    """環境変数で指定されたフォントのパスを取得する

    指定がないときは None を返す。
    指定されたフォントを使えないときは、フォールバックせずに例外にする
    """
    font = os.environ.get(FONT_ENVVAR)
    if not font:
        return None

    try:
        return _resolve(font)
    except (OSError, RuntimeError) as e:
        # どの環境変数が原因なのかわかるようにする
        msg = f"cannot use the font specified by {FONT_ENVVAR}: {font}"
        raise OSError(msg) from e


def japanize(font=None, *, italic=None, bold=None, bold_italic=None, name=None):
    """日本語を表示できるフォントを Kivy に登録する

    :param font: 使用するフォントファイルのパス。
                 省略すると環境変数 JAPANIZE_KIVY_FONT、それもなければ同梱の IPAex ゴシックを使う。
                 指定されたフォントを使えないときは、別のフォントで代替せずに例外にする
    :param italic: 斜体に使うフォントファイルのパス。省略すると font と同じものを使う
    :param bold: 太字に使うフォントファイルのパス。省略すると font と同じものを使う
    :param bold_italic: 太字かつ斜体に使うフォントファイルのパス。省略すると bold、italic、font の順に使う
    :param name: 登録する名前。省略すると Kivy の既定のフォント名になり、アプリケーション全体に適用される
    :return: 登録した名前
    :raises OSError: 指定されたフォントファイルを読めないとき
    """
    if font is None:
        font = _font_from_environ() or BUNDLED_FONT_PATH

    if name is None:
        name = DEFAULT_FONT

    if bold_italic is None:
        # Kivy は指定のないスロットに regular を入れてしまうため、近いスタイルを補っておく
        bold_italic = bold if bold is not None else italic

    # 登録する前にすべて解決して、失敗したときに状態を変えないようにする
    styles = [_resolve(style) if style is not None else None for style in (italic, bold, bold_italic)]
    regular = _resolve(font)

    # 同梱しているフォントは、別のフォントに差し替えても使えるようにしておく
    resource_add_path(str(RESOURCE_PATH))
    LabelBase.register(BUNDLED_FONT_NAME, str(BUNDLED_FONT_PATH))

    LabelBase.register(name, regular, *styles)

    return name


def show_license():
    license_agreement_filepath = RESOURCE_PATH / "IPA_Font_License_Agreement_v1.0.txt"
    # ファイルは BOM 付きの UTF-8 になっている
    license_agreement = license_agreement_filepath.read_text(encoding="utf-8-sig")
    print(license_agreement, file=sys.stderr)  # ruff: ignore[print]
