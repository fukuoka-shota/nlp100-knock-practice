str1 = "パトカー"
str2 = "タクシーあいうえお"

result_list = []
for a, b in zip(str1, str2):
    result_list.append(a+b)
ans = ''.join(result_list)
print(ans)