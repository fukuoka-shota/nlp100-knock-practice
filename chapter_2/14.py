n = 10

with open("popular-names.txt") as f:
    lines = f.readlines()
    for i in range(10):
        print(lines[i].rstrip().split()[0])

#unixコマンド回答
#head -10 popular-names.txt | cut -f 1 -d $'\t'
#cutコマンドで各行から指定した部分を切り出す、-fオプションで指定した文字で区切り、出力する要素の順番の番号を指定、$'\t'でasciiコードを展開