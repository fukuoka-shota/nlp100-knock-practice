import gzip
import json

file_name = 'jawiki-country.json.gz'

#rtはread text 
#1行1記事だから、for文で1記事(line)を取り出す
#json.loads()の返り値は辞書型
with gzip.open(file_name, 'rt', encoding='utf-8') as f:
    for line in f:
        article = json.loads(line)
        if article['title'] == 'イギリス':
            print(article['text'])
            break