import pandas as pd 

def load_morpheme_txt(path):
    rows = []
    with open (path, "r", encoding="utf-8") as f:
        for line in f:
            if line == "EOS":
                break
            #曖昧性(@で始まる行)のある形態素の２つ目の要素を読み飛ばす
            if line.startswith("@"):
                continue

            parts = line.split(" ")
            rows.append(parts[:4])
    df = pd.DataFrame(rows, columns=["表記","読み","原型","品詞"])
    return df

df = load_morpheme_txt("juman_result_UTF8.txt")
# print(df.head())

noun_phrases = []

# 先頭と末尾はスキップ（前後の語が存在しないため）
for index in range(1, len(df) - 1):
    current_word = df.iloc[index]
    prev_word = df.iloc[index - 1]
    next_word = df.iloc[index + 1]

    # 条件：「の」かつ前後が名詞
    if current_word["表記"] == "の":
        if prev_word["品詞"] == "名詞" and next_word["品詞"] == "名詞":
            phrase = f"{prev_word['表記']}の{next_word['表記']}"
            noun_phrases.append(phrase)

# 結果を表示
print(noun_phrases)