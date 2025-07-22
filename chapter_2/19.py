import pandas as pd

with open("popular-names.txt") as f:
    lines = f.readlines()
    each_line_list = []
    for line in lines:
        each_line_list.append(list(line.split()))
    df = pd.DataFrame(each_line_list)
    df[2] = df[2].astype(int)
    result = df.sort_values(by=2, ascending=False)
    print(result)

#unixコマンド回答
#sort -rnk 3 popular-names.txt
#-nで数字、-rでreverse、-kで列数の指定