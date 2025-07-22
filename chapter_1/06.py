def n_gram(str, n):
    return [str[i:i+n] for i in range((len(str)) - n + 1)]

str1 = "paraparaparadise"
str2 = "paragraph"

X = n_gram(str1, 2)
Y = n_gram(str2, 2)

x_union_y = set(X) | set(Y)
x_and_y = set(X) & set(Y)
x_minus_y = set(X) - set(Y)

print(x_union_y)
print(x_and_y)
print(x_minus_y)