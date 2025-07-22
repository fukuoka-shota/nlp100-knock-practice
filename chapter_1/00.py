str1 = "パトカー"
str2 = "タクシー"

comb_str1_str2 = zip(str1, str2)
ans = ''.join(a+b for a, b in comb_str1_str2)
print(ans)