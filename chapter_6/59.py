import gensim
import numpy as np
from scipy.cluster.hierarchy import dendrogram
from sklearn.manifold import TSNE

model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

path = "./単語アナロジーの評価データ.txt"
with open(path) as f:
    text_list = f.readlines()

text_list = list(map(lambda x: x.strip(),text_list))

country_list = []

for line_list in text_list:
    if line_list == ": capital-common-countries" or line_list ==": capital-world":
        continue
    if line_list == ": currency":
        break
    four_element = line_list.split()
    country_list.append(four_element[1])
    country_list.append(four_element[3])

unique_country_list = list(set(country_list))

country_wv_list = []
for country_wv in unique_country_list:
    country_wv_list.append(model[f"{country_wv}"])

X = np.array(country_wv_list)

X_embedded = TSNE(n_components=2, learning_rate='auto',init='random', perplexity=3).fit_transform(X)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))

for i, country in enumerate(unique_country_list):
    x, y = X_embedded[i, 0], X_embedded[i, 1]
    plt.scatter(x, y, s=30, c="blue")  # 点を描画
    plt.text(x+0.5, y+0.5, country, fontsize=9)  # 国名ラベルを少しずらして描画

plt.title("t-SNE visualization of countries", fontsize=14)
plt.xlabel("t-SNE dimension 1")
plt.ylabel("t-SNE dimension 2")
plt.show()