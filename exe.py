import MeCab

# 使用している辞書ファイルのパスを確認
dicinfo = MeCab.Model().dictionary_info()
print(dicinfo.filename)