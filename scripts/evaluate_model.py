import json
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sklearn.metrics import accuracy_score, f1_score

def load_model_and_tokenizer(model_path):
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer

def evaluate_model(model, tokenizer, eval_dataset):
    model.eval()
    predictions, true_labels = [], []

    for batch in eval_dataset:
        inputs = tokenizer(batch['text'], padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predictions.extend(torch.argmax(logits, dim=-1).tolist())
            true_labels.extend(batch['labels'])

    return predictions, true_labels

def calculate_metrics(predictions, true_labels):
    accuracy = accuracy_score(true_labels, predictions)
    f1 = f1_score(true_labels, predictions, average='weighted')
    return accuracy, f1

def main():
    model_path = "models/fine_tuned_model"  # Update with your model path
    eval_dataset = []  # Load your evaluation dataset here

    model, tokenizer = load_model_and_tokenizer(model_path)
    predictions, true_labels = evaluate_model(model, tokenizer, eval_dataset)
    accuracy, f1 = calculate_metrics(predictions, true_labels)

    results = {
        "accuracy": accuracy,
        "f1_score": f1
    }

    with open("evaluation_results.json", "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    main()