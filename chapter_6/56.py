import pandas as pd
import gensim

model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

df = pd.read_csv("combined.tab", delimiter="\t")
df = df.iloc[:,[0,1,2]]

df = df.sort_values(by="Human (mean)",ascending=False).reset_index(drop=True)

df["human_rank"] = df.index + 1

df["wv"] = 0

df["wv"] = df.apply(lambda row: model.similarity(str(row["Word 1"]), str(row["Word 2"])),axis=1)
df["wv_rank"] = df["wv"].rank(method="first", ascending=False).astype(int)

print(df.head())
print(df.tail())

sigma = 0
N = 0
for i in range(len(df)):
    sigma += (df.iloc[i]["human_rank"]-df.iloc[i]["wv_rank"]) ** 2
    if i == len(df)-1:
        N = i + 1

r_spearman = 1 - (6*sigma)/(N*(N**2-1))
print("{:.3f}".format(r_spearman))