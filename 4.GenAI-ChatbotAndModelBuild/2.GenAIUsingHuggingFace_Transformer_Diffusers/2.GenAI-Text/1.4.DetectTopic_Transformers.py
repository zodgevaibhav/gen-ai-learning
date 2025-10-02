from transformers import pipeline, logging

logging.set_verbosity_error()

classifier = pipeline(
    "text-classification",
    model="cardiffnlp/tweet-topic-21-multi",
    device="mps",          # "cuda:0" for NVIDIA, -1 for CPU
    top_k=5
)

result = classifier("Oh great, another Monday morning meeting at 7am")
print(result[0][:5])  # first 5 topic scores
