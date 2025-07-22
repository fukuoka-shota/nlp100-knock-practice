n = 5
#.readline()メソッドでファイルから１行を読み取る、.rstrip()メソッドで文末の改行を削除し、print()関数の改行と２重改行にならないようにした
with open("popular-names.txt") as f:
    for i in range(n):
        print(f.readline().rstrip())

#unixコマンド回答
#head -5 popular-names.txt
#headコマンドはファイルの最初の数行を出力する 、-nオプション(nは10進数の整数値)で表示する行数を指定