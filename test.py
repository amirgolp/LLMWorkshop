import torch
import json
from transformers import AutoTokenizer, LlamaForCausalLM, Trainer, TrainingArguments
from torch.utils.data import Dataset

torch.cuda.empty_cache()

model_path = "unsloth/llama-3-8b-bnb-4bit"
peft_model_id = "ybelkada/opt-350m-lora"


tokenizer = AutoTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(
    model_path,
    use_cache=False
)
model.load_adapter(peft_model_id)


for param in model.parameters():
    param.data = param.data.float()
    param.requires_grad = True


def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    processed_texts = []
    for item in data:
        prompt = item['prompt']
        response = item['response']
        combined_text = f"{prompt} Response: {response}"
        processed_texts.append(combined_text)
    return processed_texts


texts = load_data('prompts/all_prompts.json')

inputs = tokenizer(texts, return_tensors="pt", padding="max_length", truncation=True, max_length=512)


class TextDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __len__(self):
        return len(self.encodings.input_ids)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = item['input_ids'].clone()  # labels are required for loss calculation
        return item


train_dataset = TextDataset(inputs)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer
)

trainer.train()

model.save_pretrained("query_model")