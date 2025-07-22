import random

with open("popular-names.txt") as f:
    lines = f.readlines()
    shuffled_lines = random.sample(lines,k=len(lines))
    for i in range(len(shuffled_lines)):
        print(shuffled_lines[i].rstrip())

#unixコマンド回答
#shuf popular-names.txt
#shuf file名で行でshuffle