import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

def load_data(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()

def fine_tune_model(model_name, train_data, output_dir, training_args):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Tokenize the training data
    train_encodings = tokenizer(train_data, truncation=True, padding=True)

    # Create a dataset
    class CustomDataset(torch.utils.data.Dataset):
        def __init__(self, encodings):
            self.encodings = encodings

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            return item

        def __len__(self):
            return len(self.encodings['input_ids'])

    train_dataset = CustomDataset(train_encodings)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=training_args['num_train_epochs'],
        per_device_train_batch_size=training_args['per_device_train_batch_size'],
        save_steps=training_args['save_steps'],
        save_total_limit=training_args['save_total_limit'],
        logging_dir='./logs',
        logging_steps=training_args['logging_steps'],
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
    )

    # Fine-tune the model
    trainer.train()
    trainer.save_model(output_dir)

if __name__ == "__main__":
    config_path = 'configs/fine_tuning_config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)

    train_data = load_data(config['train_data_path'])
    fine_tune_model(config['model_name'], train_data, config['output_dir'], config['training_args'])