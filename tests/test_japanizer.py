#!/usr/bin/env python

import subprocess
import sys

import pytest
from kivy.core.text import DEFAULT_FONT
from kivy.core.text import LabelBase

import japanize_kivy
from japanize_kivy.japanizer import BUNDLED_FONT_NAME
from japanize_kivy.japanizer import BUNDLED_FONT_PATH
from japanize_kivy.japanizer import FONT_ENVVAR


@pytest.fixture(autouse=True)
def clean_environ(monkeypatch):
    """実行環境の指定がテストに影響しないようにする"""
    monkeypatch.delenv(FONT_ENVVAR, raising=False)


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


@pytest.fixture
def style_fonts(tmp_path):
    """スタイルごとに区別できるフォントに見立てたファイル"""
    fonts = {}
    for style in ("italic", "bold", "bold_italic"):
        path = tmp_path / f"user-{style}.ttf"
        path.write_bytes(BUNDLED_FONT_PATH.read_bytes())
        fonts[style] = path
    return fonts


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
    # 既定のフォントが書き換わったことを確実に検出できる値を入れておく
    sentinel = ("sentinel.ttf",) * 4
    registered_fonts[DEFAULT_FONT] = sentinel

    name = japanize_kivy.japanize(user_font, name="mincho")

    assert name == "mincho"
    assert registered_fonts["mincho"][0] == str(user_font)
    assert registered_fonts[DEFAULT_FONT] == sentinel


def test_styles(registered_fonts, user_font, style_fonts):
    """スタイルごとに別のフォントを指定できる"""
    japanize_kivy.japanize(
        user_font,
        italic=style_fonts["italic"],
        bold=style_fonts["bold"],
        bold_italic=style_fonts["bold_italic"],
    )

    regular, italic, bold, bold_italic = registered_fonts[DEFAULT_FONT]
    assert regular == str(user_font)
    assert italic == str(style_fonts["italic"])
    assert bold == str(style_fonts["bold"])
    assert bold_italic == str(style_fonts["bold_italic"])


def test_style_without_specification(registered_fonts, user_font):
    """指定のないスタイルには regular と同じフォントが使われる"""
    japanize_kivy.japanize(user_font)

    assert registered_fonts[DEFAULT_FONT] == (str(user_font),) * 4


def test_bold_italic_falls_back_to_bold(registered_fonts, user_font, style_fonts):
    """bold だけ指定したときは bold_italic にも bold が使われる"""
    japanize_kivy.japanize(user_font, bold=style_fonts["bold"])

    _, italic, bold, bold_italic = registered_fonts[DEFAULT_FONT]
    assert bold == bold_italic == str(style_fonts["bold"])
    assert italic == str(user_font)


def test_bold_italic_falls_back_to_italic(registered_fonts, user_font, style_fonts):
    """italic だけ指定したときは bold_italic にも italic が使われる"""
    japanize_kivy.japanize(user_font, italic=style_fonts["italic"])

    _, italic, bold, bold_italic = registered_fonts[DEFAULT_FONT]
    assert italic == bold_italic == str(style_fonts["italic"])
    assert bold == str(user_font)


def test_environ(registered_fonts, user_font, monkeypatch):
    """環境変数でフォントを指定できる"""
    monkeypatch.setenv(FONT_ENVVAR, str(user_font))

    japanize_kivy.japanize()

    assert registered_fonts[DEFAULT_FONT][0] == str(user_font)


def test_environ_with_missing_font(registered_fonts, monkeypatch):
    """環境変数のフォントが見つからないときはフォールバックせずに例外になる"""
    monkeypatch.setenv(FONT_ENVVAR, "/nonexistent/font.ttf")
    before = dict(registered_fonts)

    with pytest.raises(OSError, match=FONT_ENVVAR):
        japanize_kivy.japanize()

    assert dict(registered_fonts) == before


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
    with pytest.raises(OSError) as excinfo:
        japanize_kivy.japanize("/nonexistent/font.ttf")

    assert excinfo.value.filename == "/nonexistent/font.ttf"


def test_unresolvable_font(registered_fonts, tmp_path, monkeypatch):
    """Kivy のリソースパスに解決を任せず、見つからなければ例外になる"""
    monkeypatch.chdir(tmp_path)
    before = dict(registered_fonts)

    # 同梱のフォントと同じファイル名でも、指定された場所になければ例外にする
    with pytest.raises(OSError):
        japanize_kivy.japanize("ipaexg.ttf")

    assert dict(registered_fonts) == before


def test_broken_environ(registered_fonts, monkeypatch):
    """環境変数の指定を解決できないときもフォールバックせずに例外になる"""
    monkeypatch.setenv(FONT_ENVVAR, "~nosuchuser42/fonts/font.ttf")

    with pytest.raises(OSError, match=FONT_ENVVAR):
        japanize_kivy.japanize()


def test_custom_font_can_render(registered_fonts, user_font):
    """登録したフォントで実際に日本語を描画できる"""
    from kivy.core.text import Label as CoreLabel

    japanize_kivy.japanize(user_font)

    label = CoreLabel(font_size=32)
    label.resolve_font_name()

    assert label.options["font_name_r"] == str(user_font)
    # 全角で描画されていれば 1 文字あたり font_size と同じ幅になる
    assert label.get_extents("こんにちは、世界") == (32 * 8, 32)


def test_directory(registered_fonts, tmp_path):
    """ファイル以外を指定したときは例外になる"""
    with pytest.raises(OSError, match="font file expected"):
        japanize_kivy.japanize(tmp_path)


def test_relative_path(registered_fonts, tmp_path, monkeypatch):
    """カレントディレクトリが変わっても指定したフォントが登録される"""
    for name in ("a", "b"):
        directory = tmp_path / name
        directory.mkdir()
        (directory / "same.ttf").write_bytes(BUNDLED_FONT_PATH.read_bytes())

    for name in ("a", "b"):
        monkeypatch.chdir(tmp_path / name)
        japanize_kivy.japanize("same.ttf")

        assert registered_fonts[DEFAULT_FONT][0] == str(tmp_path / name / "same.ttf")


def test_public_names():
    """利用者が直接書く名前は変わっていない"""
    assert FONT_ENVVAR == "JAPANIZE_KIVY_FONT"
    assert BUNDLED_FONT_NAME == "ipaexg"


def test_registered_on_import(monkeypatch):
    """インポートしただけで同梱のフォントが登録される"""
    monkeypatch.setenv("KIVY_NO_ARGS", "1")
    monkeypatch.setenv("KIVY_NO_CONSOLELOG", "1")
    script = (
        "import japanize_kivy;"
        "from kivy.core.text import DEFAULT_FONT, LabelBase;"
        "print(LabelBase._fonts[DEFAULT_FONT][0])"
    )

    completed = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        check=True,
    )

    assert completed.stdout.strip() == str(BUNDLED_FONT_PATH)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
