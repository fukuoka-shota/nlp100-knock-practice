import gensim
from sklearn.cluster import KMeans
import numpy as np
from collections import defaultdict

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

kmeans = KMeans(n_clusters=5,random_state=42,n_init="auto").fit(X)

clastered_label = kmeans.labels_
clastered_label = clastered_label.tolist()

claster_word_list = []

for i in range(5):
    for j in range(len(clastered_label)):
        if clastered_label[j] == i:
            claster_word_list.append((i,unique_country_list[j]))

defaultdict_word_clastered = defaultdict(list)
for k,v in claster_word_list:
    defaultdict_word_clastered[k].append(v)

print(defaultdict_word_clastered)