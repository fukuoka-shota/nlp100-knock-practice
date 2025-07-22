def template_sentence(x, y, z):
    snt = str(x) + "時の" + str(y) + "は" + str(z)
    return snt

x = 12
y = "気温"
z = 22.4

rtn = template_sentence(x, y, z)
print(rtn)