str = "パタトクカシーー"
str_join = []

for a in range(len(str)):
    if a != 0 and a % 2 != 0:
        str_join.append(str[a])

ans = ''.join(str_join)
print(ans)
