n = 5

with open("popular-names.txt") as f:
    lines = f.readlines()
    for i in reversed(range(n)):
        print(lines[-1-i].rstrip())

#unixコマンド
#head -5 popular-names.txt
#tailコマンドはファイルの末尾の行を取得する、-n(nは10進数の整数)オプションで指定した行数分を取得する 
