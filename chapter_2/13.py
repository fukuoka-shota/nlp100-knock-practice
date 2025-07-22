n = 10
with open("popular-names.txt") as f:
    for i in range(n):
        print(f.readline().rstrip().replace("\t","\u0020"))

#unixコマンド回答
#sed 's/    / /g' popular-names.txt | head -10 入力するときはCtrl+V→Tab
#sed 's/置換前/置換後/g' で置換ができる。gで置換することを指定する(dは削除)