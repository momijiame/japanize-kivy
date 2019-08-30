#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import japanize_kivy


class GreetingApp(App):

    def build(self):
        main_screen = BoxLayout()
        label = Label(text='こんにちは、世界')
        main_screen.add_widget(label)
        return main_screen


def main():
    # ライセンス表示
    japanize_kivy.show_license()
    # 日本語を含むアプリケーションを表示する
    app = GreetingApp()
    app.run()


if __name__ == '__main__':
    main()