import MeCab
import pandas as pd 

text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。
"""

tagger = MeCab.Tagger()
result_str = tagger.parse(text)

def convert_str_to_df(str):
    lines = str.strip().split('\n')
    morphemes = []
    
    for line in lines:
        if line == 'EOS':
            break
        parts = line.split('\t')

        morpheme = {
            '表層形': parts[0],
            '読み': parts[1] if len(parts) > 1 else '',
            '発音': parts[2] if len(parts) > 2 else '',
            '語彙素': parts[3] if len(parts) > 3 else '',
            '品詞': parts[4] if len(parts) > 4 else '',
            '活用型': parts[5] if len(parts) > 5 else '',
            '活用形': parts[6] if len(parts) > 6 else ''
        }
        morphemes.append(morpheme)
    return pd.DataFrame(morphemes, columns = ['表層形', '読み', '発音', '語彙素', '品詞', '活用型', '活用形'])

df = convert_str_to_df(result_str)
# print(df.shape)
print(df.loc[0])
