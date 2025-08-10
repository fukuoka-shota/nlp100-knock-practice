import gzip
import json
import re

file_path = 'jawiki-country.json.gz'
uk_text = ''

with gzip.open(file_path, 'rt', encoding='utf-8') as f:
    for line in f:
        article = json.loads(line)
        if article['title'] == 'イギリス':
            uk_text = article['text']
            break

#textを改行ごとに分割→リスト
lines = uk_text.splitlines()

category_lines = []
#re.match(r'', str)はstr内に''の正規表現があるかどうか、ない場合None, ある場合Match objectを返す。pythonは0以外は真より、booleanとして捉えることができる
for line in lines:
    if re.match(r'^\[\[Category:', line):
        category_lines.append(line)

#.は改行以外の任意の文字、+は直前の正規表現の１回以上の繰り返し、?は直前の正規表現を0回か1回繰り返したもの(例えば、ab?はaとabにマッチする)、group、(?:)は非キャプチャグループ
#(?:)?は非キャプチャグループが存在しても、しなくても良いことを表す
for category_line in category_lines:
    if re.match(r'\[\[Category:(.+?)(?:\|.*)?\]\]', category_line):
        print((re.match(r'\[\[Category:(.+?)(?:\|.*)?\]\]', category_line)).group(1))