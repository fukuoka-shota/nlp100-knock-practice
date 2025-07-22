import random

def typoglycemia(sentence):
    conversion_sentence = []
    words = sentence.split()
    for word in words:
        if len(word) <= 4:
            conversion_sentence.append(word)
        else:
            middle = list(word[1:-1])
            random.shuffle(middle)
            shuffled = word[0] + ''.join(middle) + word[-1]
            conversion_sentence.append(shuffled)
    return ' '.join(conversion_sentence)

        
example = "I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
print(typoglycemia(example))
