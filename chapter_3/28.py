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
    \s*     #1文字のスペース
    =      #1文字の=
    \s*     #1文字のスペース
    (.+?)   #キャプチャ対象、任意の1文字以上
    (?:		# キャプチャ対象外のグループ開始
        (?=\n\|) 	# (?=...)...が次に次ぐクモノにマッチすれば、マッチするが文字列を消費しない(先読みアサーション)
        | (?=$)     #| はまたはの意味、(?=$)は最後の行を含むようにするため、$は文字列の末尾
    )			# グループ終了
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

    #内部リンクの除去
    #除去しないもの
    #[[ファイル:Royal Coat of Arms of the United Kingdom.svg|85px|イギリスの国章]]
    #除去するもの
    #（[[イギリスの国章|国章]]）→(国章)
    #
    #貪欲はできるだけ多く、非貪欲はできるだけ少なく
    prog = re.compile(r"""
                    \[\[
                    (?:[^|]*\|)?? #(?:)は非キャプチャ、[^a]でaでない文字、*は０回以上、?は直前を0回か1回、次の?は非貪欲
                    ([^|]*?)
                    \]\]
    """, re.VERBOSE)
    #re.subでマッチ全体を、キャプチャ１の内容に置き換える。マッチ外の部分はそのまま残る。以下、例
    #通貨 [[スターリング・ポンド|UKポンド]] (£)        (マッチは]]まで)
    #通貨 UKポンド (£)
    markup_removed = {k : prog.sub(r"\1", v) for k, v in markup_removed.items()}

    #{{...}}の外側の波かっこの除去
    prog = re.compile(r"""
                      \{\{
                      (.*?)
                      \}\}
                      """, re.DOTALL | re.VERBOSE)
    markup_removed = {k : prog.sub(r"\1", v) for k, v in markup_removed.items()}

    return markup_removed

markup_removed = markup_remove(dictionaly_object_of_template)

#確認用
# for k, v in markup_removed.items():
#     print(k,v)

#マークアップだと思われるものを除去する関数を定義(Help:早見表に書かれていないもの)
def markup_remove_extra(markup_removed):
    #</ref>の除去
    markup_removed_extra = {k : re.sub(r"<\/ref>", '', v) for k, v in markup_removed.items()}
    #<ref>の除去
    markup_removed_extra = {k : re.sub(r"<ref>", '', v) for k, v in markup_removed_extra.items()}  
    #<br />の除去
    markup_removed_extra = {k : re.sub(r"<br \/>", '', v) for k, v in markup_removed_extra.items()}
    #[[ ]]の除去
    prog = re.compile(r"""
                      \[\[
                      (.*?)
                      \]\]
                      """, re.DOTALL | re.VERBOSE)
    markup_removed_extra = {k : prog.sub(r"\1", v) for k, v in markup_removed_extra.items()}
    return markup_removed_extra
    

markup_removed_extra = markup_remove_extra(markup_removed)

#確認用
for k, v in markup_removed_extra.items():
    print(k,v)