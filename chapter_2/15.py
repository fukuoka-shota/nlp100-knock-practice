n = 10

#ファイルの行数の取得
with open("popular-names.txt") as f:
    all_lines_nbr = sum([1 for _ in f])

#分割後の行数の取得
split_file_lines_nbr = int(all_lines_nbr / 10)

with open("popular-names.txt") as f:
    for i in range(n):
        split_txt = ""
        for j in range(split_file_lines_nbr):
            split_txt += f.readline()
        try:
            with open(f"split_flie_{i}", mode="x") as f_out:
                f_out.write(split_txt)
        except FileExistsError:
            pass


#$()でコマンドの実行結果に置き換わる、 「<」は標準入力(ファイルの中身のみを入力とする)
#=で変数に代入、(シェル内の変数の仕組みがわからない...)

#LINES=$(wc -l < popular-names.txt)
#SPLIT_LINES=$(( (LINES + 9) / 10 ))
#split -l $SPLIT_LINES popular-names.txt split_

