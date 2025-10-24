from transformers import AutoTokenizer

model_id = "answerdotai/ModernBERT-base"
tokenizer = AutoTokenizer.from_pretrained(model_id)

text = "The movie was full of incomprehensibilities."
inputs = tokenizer(text, return_tensors="pt")

# トークン列を文字列で表示
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
print(tokens)
