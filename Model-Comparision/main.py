# 🧠 LLaMA Model Comparator Tool

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from IPython.display import display, Markdown
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Hugging Face token from environment
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
DEVICE = os.getenv("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
MAX_MEMORY = int(os.getenv("MAX_MEMORY", 16)) * (1024 * 1024 * 1024)  # Convert GB to bytes

MODEL_INFO = {
    "base": {
        "id": "meta-llama/Llama-2-7b-hf",
        "summary": "🧩 Base model without fine-tuning. Not optimized for dialogue or instruction following.",
        "context_length": 4096
    },
    "instruct": {
        "id": "meta-llama/Llama-2-7b-chat-hf",
        "summary": "🗣️ Chat-tuned model, optimized for following instructions using supervised fine-tuning + RLHF.",
        "context_length": 4096
    },
    "finetuned": {
        "id": "NousResearch/Llama-2-7b-chat-hf",
        "summary": "🧪 Fine-tuned instruct model by NousResearch. Specialized on longer chats and niche tasks.",
        "context_length": 4096
    }
}

def load_model_and_tokenizer(model_key):
    model_id = MODEL_INFO[model_key]['id']
    print(f"Loading {model_id} ...")
    
    # Use Hugging Face token for authentication
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)
    
    # Configure device and memory settings
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        token=HF_TOKEN,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
        device_map="auto",
        max_memory={0: f"{MAX_MEMORY}"} if DEVICE == "cuda" else None
    )
    return tokenizer, model

def generate_response(prompt, model_key):
    tokenizer, model = load_model_and_tokenizer(model_key)
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    input_length = inputs.input_ids.shape[1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            repetition_penalty=1.1,
            eos_token_id=tokenizer.eos_token_id
        )

    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    total_tokens = outputs.shape[1]
    
    return output_text.strip(), input_length, total_tokens

def plot_token_usage(input_tokens, output_tokens, context_limit):
    labels = ['Input Tokens', 'Output Tokens', 'Remaining Capacity']
    values = [input_tokens, output_tokens - input_tokens, max(0, context_limit - output_tokens)]
    colors = ['#FF9999','#99CCFF','#C1E1C1']

    plt.figure(figsize=(7, 4))
    plt.bar(labels, values, color=colors)
    plt.title("📊 Token Usage Breakdown")
    plt.ylabel("Tokens")
    for i, v in enumerate(values):
        plt.text(i, v + 20, str(v), ha='center', fontweight='bold')
    plt.ylim(0, context_limit + 300)
    plt.show()

def compare_model(prompt, model_key):
    print(f"\n=== {model_key.upper()} MODEL ===")
    model_data = MODEL_INFO[model_key]

    # Show summary
    display(Markdown(f"### 🔍 Model Summary\n{model_data['summary']}"))

    # Generate
    response, input_tokens, total_tokens = generate_response(prompt, model_key)
    
    # Show response
    display(Markdown(f"### 🧠 Response\n```\n{response}\n```"))

    # Show token stats
    print(f"Input Tokens: {input_tokens}")
    print(f"Total Tokens Used: {total_tokens}")
    print(f"Model Max Context: {model_data['context_length']}")
    
    # Plot
    plot_token_usage(input_tokens, total_tokens, model_data['context_length'])

def main():
    print("🧠 LLaMA Model Comparator Tool")
    print("-----------------------------")
    
    if not HF_TOKEN:
        print("⚠️ Warning: No Hugging Face token found in environment variables.")
        print("Please create a .env file with your HUGGINGFACE_TOKEN.")
        print("See .env.example for reference.")
        return
    
    # === 🔧 Interactive Input ===
    prompt = input("Enter your prompt: ")
    model_type = input("Choose model type [base/instruct/finetuned]: ").strip().lower()

    if model_type not in MODEL_INFO:
        print("Invalid model type. Please choose from: base, instruct, finetuned")
    else:
        compare_model(prompt, model_type)

if __name__ == "__main__":
    main()
