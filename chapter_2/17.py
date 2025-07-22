with open("popular-names.txt") as f:
    lines = f.readlines()
    name_list = []
    for i in range(len(lines)):
        name_list.append(lines[i].split()[0])
    setted_name_list = set(name_list)
    print(len(setted_name_list))

#unixコマンド回答
#cut -f 1 -d $'\t' popular-names.txt | sort | uniq
#cutコマンドで各行から指定した部分を切り出す、-fオプションで指定した文字で区切り、出力する要素の順番の番号を指定、$'\t'でasciiコードを展開、dは特殊文字を扱うためのオプション | sortで並び替える(uniqは連続していないといけない) | uniqで重複を削除