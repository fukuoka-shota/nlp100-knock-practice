sentence = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
#replaceでピリオドを消す、splitでスペースで単語を分割し、リストにする
words = sentence.replace('.', '').split()
# print(words)
number = {1, 5, 6, 7, 8, 9, 15, 16, 19}
dict = {}

for i, word in enumerate(words, 1):
    if i in number:
        extracted_chars = word[0]
    else:
        extracted_chars = word[:2]
    dict[extracted_chars] = i

print(dict)