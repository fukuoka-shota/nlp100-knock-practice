def n_gram(str, n):
    return [str[i:i+n] for i in range((len(str)) - n + 1)]

sentence = "I am an NLPer"
words = sentence.split()
word_bi_gram = n_gram(words, 2)
char_tri_gram = n_gram(sentence, 3)
print(word_bi_gram,char_tri_gram)


