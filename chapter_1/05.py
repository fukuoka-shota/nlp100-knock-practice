def n_gram(str, n):
    return [str[i:i+n] for i in range((len(str)) - n + 1)]

