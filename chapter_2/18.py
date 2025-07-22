import collections

with open("popular-names.txt") as f:
    lines = f.readlines()
    name_list = []
    for i in range(len(lines)):
        name_list.append(lines[i].split()[0])
    frequency_of_appearance_list = collections.Counter(name_list)
    for name, count in frequency_of_appearance_list.most_common():
        print(name, count)

#unixコマンド回答
#cut -f 1 -d $'\t' popular-names.txt | sort | uniq -c | sort -nr
#cutコマンドで各行から指定した部分を切り出す、-fオプションで指定した文字で区切り、出力する要素の順番の番号を指定、$'\t'でasciiコードを展開、dは特殊文字を扱うためのオプション | sortで並び替える(uniqは連続していないといけない) | uniqで重複を削除 | sort -nr のオプションで数字順、rで降順にしている