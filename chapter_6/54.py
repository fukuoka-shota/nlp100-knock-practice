import gensim

model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

path = "./単語アナロジーの評価データ.txt"
with open(path) as f:
    text_list = f.readlines()

text_list = list(map(lambda x: x.strip(),text_list))

correct_answer_count = 0
capital_common_countories_count = 0

for line_list in text_list:
    if line_list == ": capital-common-countries":
        continue
    if line_list == ": capital-world":
        break
    capital_common_countories_count += 1
    four_element = line_list.split()
    vec = model[f"{four_element[1]}"]-model[f"{four_element[0]}"]+model[f"{four_element[2]}"]
    print(model.most_similar(positive=[vec],topn=1))