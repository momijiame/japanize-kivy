#!/usr/bin/env python

import pytest
from kivy.core.text import DEFAULT_FONT
from kivy.core.text import LabelBase

import japanize_kivy
from japanize_kivy.japanizer import BUNDLED_FONT_NAME
from japanize_kivy.japanizer import BUNDLED_FONT_PATH
from japanize_kivy.japanizer import FONT_ENVVAR


@pytest.fixture
def registered_fonts():
    """テストごとに Kivy に登録されているフォントを元に戻す"""
    saved = dict(LabelBase._fonts)
    yield LabelBase._fonts
    LabelBase._fonts.clear()
    LabelBase._fonts.update(saved)


@pytest.fixture
def user_font(tmp_path):
    """利用者が用意したフォントに見立てたファイル"""
    path = tmp_path / "user.ttf"
    path.write_bytes(BUNDLED_FONT_PATH.read_bytes())
    return path


def test_default_is_bundled_font(registered_fonts):
    """既定では同梱のフォントが Kivy の既定のフォント名に登録される"""
    name = japanize_kivy.japanize()

    assert name == DEFAULT_FONT
    assert registered_fonts[DEFAULT_FONT] == (str(BUNDLED_FONT_PATH),) * 4


def test_bundled_font_has_its_own_name(registered_fonts, user_font):
    """別のフォントに差し替えても同梱のフォントを名前で引ける"""
    japanize_kivy.japanize(user_font)

    assert registered_fonts[BUNDLED_FONT_NAME][0] == str(BUNDLED_FONT_PATH)


def test_custom_font(registered_fonts, user_font):
    """利用者が用意したフォントを既定にできる"""
    japanize_kivy.japanize(user_font)

    assert registered_fonts[DEFAULT_FONT] == (str(user_font),) * 4


def test_custom_font_as_str(registered_fonts, user_font):
    """フォントのパスは文字列でも指定できる"""
    japanize_kivy.japanize(str(user_font))

    assert registered_fonts[DEFAULT_FONT][0] == str(user_font)


def test_custom_name(registered_fonts, user_font):
    """別名で登録すると Kivy の既定のフォントには影響しない"""
    before = registered_fonts[DEFAULT_FONT]

    name = japanize_kivy.japanize(user_font, name="mincho")

    assert name == "mincho"
    assert registered_fonts["mincho"][0] == str(user_font)
    assert registered_fonts[DEFAULT_FONT] == before


def test_styles(registered_fonts, user_font, tmp_path):
    """スタイルごとに別のフォントを指定できる"""
    bold_font = tmp_path / "user-bold.ttf"
    bold_font.write_bytes(BUNDLED_FONT_PATH.read_bytes())

    japanize_kivy.japanize(user_font, bold=bold_font)

    regular, italic, bold, bold_italic = registered_fonts[DEFAULT_FONT]
    assert bold == str(bold_font)
    # 指定のないスタイルには regular と同じフォントが使われる
    assert regular == italic == bold_italic == str(user_font)


def test_environ(registered_fonts, user_font, monkeypatch):
    """環境変数でフォントを指定できる"""
    monkeypatch.setenv(FONT_ENVVAR, str(user_font))

    japanize_kivy.japanize()

    assert registered_fonts[DEFAULT_FONT][0] == str(user_font)


def test_environ_with_missing_font(registered_fonts, monkeypatch):
    """環境変数の指定が不正なときは同梱のフォントにフォールバックする"""
    monkeypatch.setenv(FONT_ENVVAR, "/nonexistent/font.ttf")

    japanize_kivy.japanize()

    assert registered_fonts[DEFAULT_FONT][0] == str(BUNDLED_FONT_PATH)


def test_argument_takes_precedence_over_environ(registered_fonts, user_font, tmp_path, monkeypatch):
    """引数は環境変数より優先される"""
    other_font = tmp_path / "other.ttf"
    other_font.write_bytes(BUNDLED_FONT_PATH.read_bytes())
    monkeypatch.setenv(FONT_ENVVAR, str(other_font))

    japanize_kivy.japanize(user_font)

    assert registered_fonts[DEFAULT_FONT][0] == str(user_font)


def test_home_relative_path(registered_fonts, tmp_path, monkeypatch):
    """~ から始まるパスを指定できる"""
    monkeypatch.setenv("HOME", str(tmp_path))
    font = tmp_path / "home.ttf"
    font.write_bytes(BUNDLED_FONT_PATH.read_bytes())

    japanize_kivy.japanize("~/home.ttf")

    assert registered_fonts[DEFAULT_FONT][0] == str(font)


def test_missing_font(registered_fonts):
    """指定されたフォントが見つからないときは例外になる"""
    with pytest.raises(OSError, match="not found"):
        japanize_kivy.japanize("/nonexistent/font.ttf")


def test_custom_font_can_render(registered_fonts, user_font):
    """登録したフォントで実際に日本語を描画できる"""
    from kivy.core.text import Label as CoreLabel

    japanize_kivy.japanize(user_font)

    label = CoreLabel(font_size=32)
    label.resolve_font_name()

    assert label.options["font_name_r"] == str(user_font)
    # 全角で描画されていれば 1 文字あたり font_size と同じ幅になる
    assert label.get_extents("こんにちは、世界") == (32 * 8, 32)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
