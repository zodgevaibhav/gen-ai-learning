from transformers import pipeline

pipeline = pipeline(task="image-classification", model="google/vit-base-patch16-224")
result = pipeline(images="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg")

print(result)
