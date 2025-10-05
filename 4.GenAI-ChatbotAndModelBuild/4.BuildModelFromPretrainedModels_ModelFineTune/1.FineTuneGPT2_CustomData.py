# Fine-tune GPT-2 on your text and interactively ask questions
# Install: pip install transformers datasets torch

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling, pipeline

# ----------------------------
# Step 1: Choose model
# ----------------------------
model_name = "EleutherAI/gpt-neo-2.7B"  # gpt2 small, lightweight; use "EleutherAI/gpt-neo-1.3B" for bigger models
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# GPT-2 does not have padding token by default
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# ----------------------------
# Step 2: Prepare dataset
# ----------------------------
# Save your text in a file called "my_text.txt"
# Example:
#   Hugging Face is creating amazing NLP tools.
#   Python is widely used for AI and ML.

file_path = "my_text.txt"

dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=file_path,
    block_size=128,   # max sequence length
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  # causal LM
)

# ----------------------------
# Step 3: Training
# ----------------------------
training_args = TrainingArguments(
    output_dir="./gpt2-finetuned",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=200,
    save_total_limit=2,
    logging_steps=50,
    prediction_loss_only=True,
    fp16=torch.cuda.is_available(),
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

print("🚀 Starting fine-tuning on your text...")
trainer.train()
model.save_pretrained("./gpt2-finetuned")
tokenizer.save_pretrained("./gpt2-finetuned")
print("✅ Fine-tuning complete!")

# ----------------------------
# Step 4: Interactive QnA
# ----------------------------
qa_pipeline = pipeline("text-generation", model="./gpt2-finetuned", tokenizer="./gpt2-finetuned")

print("\n🎤 Ask questions based on your text (type 'exit' to quit)")
while True:
    question = input("\nQ: ")
    if question.lower() == "exit":
        break
    prompt = f"Question: {question}\nAnswer:"
    output = qa_pipeline(prompt, max_length=150, do_sample=True, temperature=0.7)
    answer = output[0]["generated_text"].split("Answer:")[-1].strip()
    print("A:", answer)
