from importlib.metadata import version

from japanize_kivy.japanizer import BUNDLED_FONT_NAME
from japanize_kivy.japanizer import BUNDLED_FONT_PATH
from japanize_kivy.japanizer import FONT_ENVVAR
from japanize_kivy.japanizer import japanize
from japanize_kivy.japanizer import show_license

__version__ = version("japanize-kivy")

__all__ = [
    "BUNDLED_FONT_NAME",
    "BUNDLED_FONT_PATH",
    "FONT_ENVVAR",
    "japanize",
    "show_license",
]

# インポートするだけで日本語を表示できるようにするのがこのパッケージの目的
japanize()  # ruff: ignore[non-empty-init-module]
