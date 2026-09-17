# japanize-kivy

[![test](https://github.com/momijiame/japanize-kivy/actions/workflows/test.yml/badge.svg)](https://github.com/momijiame/japanize-kivy/actions/workflows/test.yml)

インポートするだけで Kivy が日本語を表示できるようになります

### インストール

pip でインストールします。

```sh
$ pip install japanize-kivy
```

### 使い方

パッケージをインポートするだけです。

```python
import japanize_kivy
```

Kivy のアプリケーションで日本語が IPAex ゴシックフォントで表示されます。

### フォントを差し替える

自分で用意したフォントを使いたいときは `japanize()` にパスを渡します。

```python
import japanize_kivy

japanize_kivy.japanize("~/fonts/NotoSansJP-Regular.ttf")
```

太字や斜体に別のファイルを使う場合は、あわせて指定します。

```python
japanize_kivy.japanize(
    "~/fonts/NotoSansJP-Regular.ttf",
    bold="~/fonts/NotoSansJP-Bold.ttf",
)
```

`name` を指定すると別名で登録されるので、特定のウィジェットにだけ使えます。
同梱の IPAex ゴシックは `japanize_kivy.BUNDLED_FONT_NAME` の名前で引けるため、差し替えても併用できます。

```python
name = japanize_kivy.japanize("~/fonts/Mincho.ttf", name="mincho")

Label(text="見出し", font_name=name)
Label(text="本文", font_name=japanize_kivy.BUNDLED_FONT_NAME)
```

コードを変えずに差し替えたいときは、環境変数 `JAPANIZE_KIVY_FONT` にパスを指定します。

```sh
$ JAPANIZE_KIVY_FONT=~/fonts/NotoSansJP-Regular.ttf python app.py
```

フォントは 引数 > 環境変数 > 同梱の IPAex ゴシック の順に優先されます。
なお、フォントはウィジェットを作る前に決めてください。
登録し直しても、生成済みのウィジェットは自動では新しいフォントに追従しません。

### サンプル

example ディレクトリ以下にサンプルがあります。

```sh
$ python example/greet.py
```

### ライセンス

同梱している IPAex ゴシックフォントを使う場合は、そのライセンスに同意してください。
自分で用意したフォントに差し替えた場合は、そのフォントのライセンスに従ってください。

ライセンスは次のように確認できます。

```python
import japanize_kivy

japanize_kivy.show_license()
```
