import json
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from torch.utils.data import Dataset


class PromptResponseDataset(Dataset):
    def __init__(self, tokenizer, path):
        self.tokenizer = tokenizer
        self.prompts, self.responses = self.load_data(path)

    def load_data(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
        prompts = [entry['prompt'] for entry in data]
        responses = [entry['response'] for entry in data]
        return prompts, responses

    def __len__(self):
        return len(self.prompts)

    def __getitem__(self, idx):
        prompt = self.prompts[idx]
        response = json.dumps(self.responses[idx])
        encoding = self.tokenizer(prompt, response, truncation=True, padding="max_length", max_length=512,
                                  return_tensors='pt')
        input_ids = encoding.input_ids.squeeze(0)
        labels = input_ids.clone()

        input_ids.requires_grad_(False)
        labels.requires_grad_(False)

        return {"input_ids": input_ids, "labels": labels}


def main():
    model_path = "unsloth/llama-3-8b-bnb-4bit"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    peft_model_id = "ybelkada/opt-350m-lora"
    model = AutoModelForCausalLM.from_pretrained(model_path)
    model.load_adapter(peft_model_id)

    model.train()

    dataset = PromptResponseDataset(tokenizer, 'all_prompts.json')
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=2,
        logging_steps=10,
        save_strategy="epoch",
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    trainer.train()


main()
