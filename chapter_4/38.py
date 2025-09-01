import gzip
import json
import re
import MeCab, ipadic
import math
from collections import Counter, defaultdict

def remove_markup(text):
    #prog_1:強調マークアップの除去
    #prog_2:内部リンクの除去
    #prog_3:外部リンクの除去 [http:...]
    #prog_4:タグ<...>の除去
    #prog_5:テンプレート{{...}}の除去
    #prog_6:基礎情報テンプレートの除去
    #prog_7:見出しの除去
    #prog_8:ファイルの除去
    #prog_9:コメントアウトの除去
    #prog_10:箇条書き(*の行)の除去、|で始まる行の削除
    #prog_11:space+|で始まる行の除去
    #prog_12:{{,}},()の削除
    #prog_13:2連続以上の改行を２の改行にする
    prog_1 = re.compile(r"'{2,5}")
    prog_2 = re.compile(r"\[\[(?:[^|]*\|)??([^|]*?)\]\]")
    prog_3 = re.compile(r"\[http[^\]]+\]")
    prog_4 = re.compile(r"\<.+?\>")
    prog_5 = re.compile(r"\{\{.*?\}\}")
    prog_6 = re.compile(r"{{基礎情報.*?\n.*?\n}}",re.DOTALL)
    prog_7 = re.compile(r"={2,}")
    prog_8 = re.compile(r"\[\[ファイル:.*?\]\]")
    prog_9 = re.compile(r"\<\!--.*--\>",re.DOTALL)
    #[]は文字の集合を表す
    prog_10 = re.compile(r"^[*#:;|].*$",re.MULTILINE)
    prog_11 = re.compile(r"^ \|.*$",re.MULTILINE)
    prog_12 = re.compile(r"\{\{|\}\}|\(\)")
    prog_13 = re.compile(r"\n{2,}")
    text = prog_1.sub("", text)
    text = prog_2.sub(r"\1", text)
    text = prog_3.sub("", text)
    text = prog_4.sub("", text)
    text = prog_5.sub("", text)
    text = prog_6.sub("", text)
    text = prog_7.sub("", text)
    text = prog_8.sub("", text)
    text = prog_9.sub("", text)
    text = prog_10.sub("", text)
    text = prog_11.sub("", text)
    text = prog_12.sub("", text)
    text = prog_13.sub("\n\n", text)

    return text

def calculate_tfidf():
    #MeCabの初期化
    mecab = MeCab.Tagger(f'-d "{ipadic.DICDIR}" -Ochasen')
    #文書をカウントするための変数
    total_docs = 0
    #各名詞が出現する文書数をカウント
    doc_freq = defaultdict(int)
    #日本に関する記事の名詞の出現頻度をカウント
    japan_noun_freq = Counter()

    # gzipファイルを読み込む
    with gzip.open("jawiki-country.json.gz", "rt", encoding="utf-8") as f:
        for line in f:
            total_docs += 1
            article = json.loads(line)
            text = article["text"]

            # マークアップを除去
            text = remove_markup(text)

            # 形態素解析を行い、名詞をカウント
            # nodeは双方向リンクリスト
            node = mecab.parseToNode(text)
            # この文書で出現した名詞を記録
            doc_nouns = set()
            while node:
                if node.feature.split(",")[0] == "名詞":
                    noun = node.surface
                    doc_nouns.add(noun)
                    # 日本に関する記事の場合、出現頻度をカウント
                    if article["title"] == "日本":
                        japan_noun_freq[noun] += 1
                node = node.next
            # 文書頻度を更新
            for noun in doc_nouns:
                doc_freq[noun] += 1

    # TF-IDFスコアを計算
    tfidf_scores = {}
    for noun, tf in japan_noun_freq.items():
        # IDFの計算
        idf = math.log(total_docs / doc_freq[noun])
        # TF-IDFスコアの計算
        tfidf_scores[noun] = {"tf": tf, "idf": idf, "tfidf": tf * idf}

    # TF-IDFスコアの高い順に20語を表示
    for noun, scores in sorted(
        tfidf_scores.items(), key=lambda x: x[1]["tfidf"], reverse=True
    )[:20]:
        print(f"{noun}:")
        print(f"  TF: {scores['tf']}")
        print(f"  IDF: {scores['idf']:.4f}")
        print(f"  TF-IDF: {scores['tfidf']:.4f}")




if __name__ == "__main__":
    calculate_tfidf()