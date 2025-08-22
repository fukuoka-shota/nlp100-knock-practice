import gzip
import json
import re

file_name = "jawiki-country.json.gz"

#イギリスのテキストを抽出する関数を定義
def extract_uk_text():
    #rtはread text
    #1行1記事だから、for文で1記事(line)を取り出す
    #json.loads()の返り値は辞書型
    with gzip.open(file_name, "rt", encoding="utf-8") as f:
        for line in f:
            article = json.loads(line)
            if article["title"] == "イギリス":
                return article["text"]

uk_text = extract_uk_text()

#基本情報が含まれていることの確認
# for i, line in enumerate(uk_text.split("\n")):
#     if i >= 75:
#         break
#     print(line)


#「基礎情報」テンプレートのフィールド名と値を抽出し、辞書オブジェクトを返す関数を定義
def dictionaly_object_of_template():
    #方針　２段階で処理
    #1step : 基礎情報テンプレートのフィールド名が含まれた行のみ抽出
    #2step : | a=b　行のaとbをキャプチャする

    #テンプレート内のフィールド名がある行だけキャプチャする
    #re.DOTALL(フラグ)で.は改行を含むすべての文字列とマッチする。デフォルトだと、.は改行にマッチしない
    #re.VERBOSE(フラグ)によって、正規表現の複数行の中の改行を無効化、コメントを可能にする
    #フラグは|(ビット演算子OR)を利用する、演算子の結果が同じにならないように設計されている
    #re.compileの返り値はre.Patternオブジェクト、メソッドとして
    prog = re.compile(r"""
                    {{基礎情報 #基礎情報テンプレートの開始
                    .*?        #国名
                    \n         #改行の次からがフィールド名
                    (.*?)      #キャプチャ、非貪欲、任意の0文字以上
                    \n}}       #最後に改行と}}が来たら終了
                    """, re.DOTALL | re.VERBOSE)

    #re.searchは最初に見つかった１つのre.Matchオブジェクトのみを返す
    #re.Matchオブジェクトの中身をgroup(1)で取得
    field_row_text = prog.search(uk_text).group(1)
    # print(field_row_text)

    #re.MULTILINE(フラグ)、^が各行の先頭にマッチし、$が各行の末尾にマッチ
    prog = re.compile(r"""
    ^\|    #|で始まる行、^は文字列の先頭
    (.+?)  #キャプチャ、非貪欲、任意の１文字以上
    \s*     #0文字以上のスペース
    =       #1文字の=
    \s*     #0文字以上のスペース
    (.*?)   #キャプチャ対象、任意の1文字以上
    (?=\n\| | \Z) 
    # (?:		# キャプチャ対象外のグループ開始
    #     (?=\n\|) 	# (?=...)...が次に続くモノにマッチすれば、マッチするが文字列を消費しない(先読みアサーション)
    #     | (?=$)     #| はまたはの意味、(?=$)は最後の行を含むようにするため、$は文字列の末尾
    # )			# グループ終了
    """, re.VERBOSE | re.MULTILINE | re.DOTALL)

    #re.findallはマッチしたパターンのストリングかタプルを返す(2つ以上の場合、タプル)
    matches = prog.findall(field_row_text)
    # print(matches)
    field_name_and_value_dict = {}
    for name, value in matches:
        field_name_and_value_dict[name] = value
    return field_name_and_value_dict

dictionaly_object_of_template = dictionaly_object_of_template()

#確認用
# for k, v in dictionaly_object_of_template.items():
#     print(k, v)

def markup_remove(dict_template):
    #強調マークアップの除去
    #{2,5}で繰り返しが2-5回にマッチさせる
    # re.sub(r"a", b, str) strのaをbに置換
    markup_removed = {k : re.sub(r"'{2,5}", '', v) for k, v in dict_template.items()}
    return markup_removed

markup_removed = markup_remove(dictionaly_object_of_template)

#確認用
for k, v in markup_removed.items():
    print(k,v)