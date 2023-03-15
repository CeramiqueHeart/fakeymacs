﻿# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## ブラウザをポップアップしてから C-l、C-t を入力するキーを設定する
####################################################################################################

try:
    # 設定されているか？
    fc.browser_list
except:
    # 本機能を適用するブラウザのプログラム名称を指定する
    fc.browser_list= ["chrome.exe",
                      "msedge.exe",
                      "firefox.exe"]

try:
    # 設定されているか？
    fc.browser_key1
except:
    # アドレスバーに移動するキーを指定する（IME は OFF）
    fc.browser_key1 = "C-A-l"

try:
    # 設定されているか？
    fc.browser_key2
except:
    # 新しいタブを開いてそのタブのアドレスバーに移動するキーを指定する（IME は OFF）
    fc.browser_key2 = "C-A-t"

# ブラウザをポップアップしてから指定したキーを実行する。

def browser_popup(key, ime_status, browser_list=fc.browser_list):
    def _func():
        for window in getWindowList():
            if window.getProcessName() in browser_list:

                # thunderbird から本コマンドを実行した際、ウィンドウフォーカスが適切に
                # 移動しない場合がある。その対策。（何かのキーを押下すると良いようだ。）
                if keymap.getWindow().getProcessName() == "thunderbird.exe":
                    self_insert_command("Shift")()

                popWindow(window)()
                delay()
                escape() # 検索状態になっていた場合に Esc で解除する
                self_insert_command(key)()
                keymap.delayedCall(lambda: setImeStatus(ime_status), 100)
                return

        # browser_list に設定されているブラウザが起動していない場合、browser_list の最初
        # に設定されているブラウザを起動する
        keymap.ShellExecuteCommand(None, browser_list[0], "", "")()

    return _func

define_key(keymap_global, fc.browser_key1, browser_popup("C-l", 0))
define_key(keymap_global, fc.browser_key2, browser_popup("C-t", 0))

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"browser_key\config_personal.py", msg=False), dict(globals(), **locals()))
