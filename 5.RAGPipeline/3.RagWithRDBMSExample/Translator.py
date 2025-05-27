# pip install transformers
# pip install sentencepiece
# pip install sacremoses


from transformers import MarianMTModel, MarianTokenizer

model_name = 'Helsinki-NLP/opus-mt-mr-en'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

text = "तुझ नाव काय आहे?"
tokens = tokenizer(text, return_tensors="pt")
translation = model.generate(**tokens)
print(tokenizer.decode(translation[0], skip_special_tokens=True))
