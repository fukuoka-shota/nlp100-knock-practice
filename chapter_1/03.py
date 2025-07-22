import string

sentence = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."

word_list = sentence.split()
word_count_list = []
for word in word_list:
    clean_word = word.strip(string.punctuation)
    word_count_list.append(len(clean_word))

print(word_count_list)