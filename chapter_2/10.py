with open("popular-names.txt") as f:
    print(sum([1 for _ in f]))

#unixコマンド回答
#wc -l popular-names.txt
#wcコマンドはファイルの行数、単語数、文字数を数える、lオプションで行数を取得