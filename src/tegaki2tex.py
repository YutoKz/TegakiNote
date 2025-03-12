"""
    手書きノートの画像をGeminiに入力、文字と数式を認識しObsidianの形式で生成
    なお、出力テキストはクリップボードに自動でコピーされる

    メモ: 
    - 画像は複数選択可能。順番はエクスプローラの上から順になる
    - PNGにエクスポートしたGoodNotesは、Dropboxで共有するのが楽かも
"""
from apikeys import GEMINI_API_KEY

import os
from google import genai
from google.genai import types
import pyperclip
import PIL.Image
from PyQt6.QtWidgets import QApplication, QFileDialog
import sys
"""
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.tk.call("tk", "scaling", 2.0) 
    file_path = filedialog.askopenfilename(parent=root)
"""
    
dropbox_path = "C:/Users/yuto1/Dropbox"
default_dir = dropbox_path if os.path.isdir(dropbox_path) else ""

app = QApplication(sys.argv)

# # 単一画像の場合
#image = PIL.Image.open(file_paths) 
#file_path, _ = QFileDialog.getOpenFileName(None, "ファイルを選択", "", "All Files (*)")
#image = PIL.Image.open(file_path)
# 複数画像の場合
file_paths, _ = QFileDialog.getOpenFileNames(None, "ファイルを選択", default_dir, "All Files (*)")
images = [PIL.Image.open(file_path) for file_path in file_paths] 

prompt = "この画像は手書きのノートである。これをObsidianにそのままペーストできる形式で出力せよ。\nなお、式変形を含むものなど長い数式は $$ $$ で囲むこと。\n出力の最初と最後に```を付ける必要はない。"

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[prompt, images]
)
print(response.text)

# クリップボードにコピー
pyperclip.copy(response.text)

