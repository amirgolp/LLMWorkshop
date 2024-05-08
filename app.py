import json
from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments
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
        response = self.responses[idx]
        input_ids = self.tokenizer(prompt, return_tensors='pt').input_ids.squeeze()
        labels = self.tokenizer(response, return_tensors='pt').input_ids.squeeze()
        return {"input_ids": input_ids, "labels": labels}


def main():
    model_path = "facebook/llama-3-70b"
    tokenizer = LlamaTokenizer.from_pretrained(model_path)
    model = LlamaForCausalLM.from_pretrained(model_path)

    # Setup LoRA adaptation
    model.set_lora_params({"r": 4})  # Adjust LoRA parameters as needed

    dataset = PromptResponseDataset(tokenizer, 'data.json')
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=2,  # Adjust batch size according to your GPU capabilities
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


if __name__ == "__main__":
    main()
