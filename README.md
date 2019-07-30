# japanize-kivy

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

### サンプル

example ディレクトリ以下にサンプルがあります。

```sh
$ python example/greet.py
```

### ライセンス

日本語の表示には IPAex ゴシックフォントを用いています。
利用される場合は IPAex ゴシックフォントのライセンスに同意してください。

ライセンスは次のように確認できます。

```python
import japanize_kivy
japanize_kivy.show_license()
```