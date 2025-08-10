#chrは10進数で指定したunicodeを文字へ変換
#ordは文字を10進数のunicode

def cipher(sentence):
    rtn = ""
    for str in sentence:
        if str.islower():
            rtn += chr(219 - ord(str))
        else:
            rtn += str
    return rtn

sentence1 = "This is a secret message."

#暗号化
print(cipher(sentence1))
#復号化
print(cipher(cipher(sentence1)))