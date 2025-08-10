import random

#タイポグリセミア（Typoglycemia）とは、文章中の単語の文字の順番が一部入れ替わっていても、文脈や単語の前後関係から、正しく読めてしまう現象のこと

def typoglycemia(sentence):
    conversion_sentence = []
    words = sentence.split()
    # print(words)
    for word in words:
        if len(word) <= 4:
            conversion_sentence.append(word)
        else:
            middle = list(word[1:-1])
            random.shuffle(middle) #破壊
            shuffled = word[0] + ''.join(middle) + word[-1]
            conversion_sentence.append(shuffled)
    return ' '.join(conversion_sentence)

        
example = "I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
print(typoglycemia(example))
