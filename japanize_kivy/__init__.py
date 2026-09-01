from japanize_kivy.japanizer import japanize
from japanize_kivy.japanizer import show_license

__version__ = "0.1.1"

__all__ = ["japanize", "show_license"]

# インポートするだけで日本語を表示できるようにするのがこのパッケージの目的
japanize()  # ruff: ignore[non-empty-init-module]
