import gensim

model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

Spain_vec = model["Spain"]
Madrid_vec = model["Madrid"]
Athens_vec = model["Athens"]

vec = Spain_vec - Madrid_vec + Athens_vec
print(vec)
print(len(vec))

print(model.most_similar(positive=[vec],topn=10))