# import torch
# from transformers import AutoModel, AutoTokenizer
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np

# # モデルとトークナイザーの読み込み
# model_id = "answerdotai/ModernBERT-base"
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModel.from_pretrained(model_id)

# # 入力文のリスト
# sentences = [
#     "The movie was full of fun.",
#     "The movie was full of excitement.",
#     "The movie was full of crap.",
#     "The movie was full of rubbish.",
# ]

# # 各文の[CLS]トークンの埋め込みベクトルを取得
# embeddings = []
# for sentence in sentences:
#     # トークン化
#     inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)

#     # モデルによる推論
#     with torch.no_grad():
#         outputs = model(**inputs)

#     # [CLS]トークンの埋め込みベクトルを取得
#     cls_embedding = outputs.last_hidden_state[0, 0, :].numpy()
#     embeddings.append(cls_embedding)

# # 埋め込みベクトルをnumpy配列に変換
# embeddings = np.array(embeddings)

# # コサイン類似度の計算（すべての組み合わせを一度に計算）
# similarity_matrix = cosine_similarity(embeddings)

# # 結果の表示
# print("文の組み合わせに対するコサイン類似度:")
# for i in range(len(sentences)):
#     for j in range(i + 1, len(sentences)):
#         print(
#             f"'{sentences[i]}' と '{sentences[j]}' の類似度: {similarity_matrix[i][j]:.4f}"
#         )

#以下確認用コードーーーーーーーーーーーーーーーーーーーーーー

import torch
from transformers import AutoModel, AutoTokenizer

model_id = "answerdotai/ModernBERT-base"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id).eval()

text = "The movie was full of fun."
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

print("=== inputs（辞書） ===")
print(type(inputs))
print(inputs.keys())              # 代表的には dict_keys(['input_ids', 'attention_mask', ...])

for k, v in inputs.items():
    print(k, v.shape, v.dtype)    # 形状とdtypeを確認
    print(v)                      # 実際のテンソル値（トークンIDやマスク）

# トークンID → トークン文字列へ
print("=== tokens ===")
print(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]))
# 例: ['[CLS]', 'The', 'Ġmovie', 'Ġwas', 'Ġfull', 'Ġof', 'Ġfun', '.', '[SEP]'] など

with torch.no_grad():
    outputs = model(**inputs)     # ここで **inputs が展開される

print("=== outputs（モデル出力の辞書風オブジェクト） ===")
print(outputs.__class__)
print(outputs.keys())             # 代表例: dict_keys(['last_hidden_state', 'pooler_output', ...])

# 各テンソルの形状
print("last_hidden_state:", outputs.last_hidden_state.shape)
# 例: torch.Size([batch, seq_len, hidden_size]) → 1, 9, 768 など
if hasattr(outputs, "pooler_output"):
    print("pooler_output:", outputs.pooler_output.shape)
    # 例: torch.Size([batch, hidden_size]) → 1, 768

# [CLS] ベクトルの中身例
cls_vec = outputs.last_hidden_state[0, 0, :]
print("CLS embedding shape:", cls_vec.shape)   # torch.Size([768]) など
print("CLS embedding (first 8 dims):", cls_vec[:8])
