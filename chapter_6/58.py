import gensim
import numpy as np
from scipy.cluster.hierarchy import dendrogram

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


from sklearn.cluster import AgglomerativeClustering
from collections import Counter

n_clusters = 2
method = "ward" # CHANGE HERE

# do clustering_moon
clustering = AgglomerativeClustering(linkage=method, n_clusters=n_clusters)
clustering.fit(X)

import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

Z = hierarchy.linkage(X, method=method)
hierarchy.dendrogram(Z, labels=unique_country_list, color_threshold=30,leaf_font_size=10 )
plt.ylabel("distance")
plt.show()