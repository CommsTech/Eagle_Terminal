import os

from transformers import AutoModelForCausalLM, AutoTokenizer


def download_and_save_model(model_name, save_path):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    os.makedirs(save_path, exist_ok=True)

    tokenizer.save_pretrained(save_path)
    model.save_pretrained(save_path)


def run(main_window):
    # Implement your model download logic here
    return "Model downloaded successfully"


if __name__ == "__main__":
    model_name = "distilgpt2"
    save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saved_model")
    download_and_save_model(model_name, save_path)
