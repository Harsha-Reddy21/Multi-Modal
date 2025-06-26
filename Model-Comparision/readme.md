
This tool allows you to compare different versions of the LLaMA-2 model family:
- **Base Model**: Untuned foundation model
- **Instruct Model**: Chat-optimized with supervised fine-tuning and RLHF
- **Fine-tuned Model**: Specialized version with additional training



## 🚀 Installation


1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Hugging Face token (see `.env.example`)

## 🔧 Usage

Run the script with:

```
python main.py
```

You'll be prompted to:
1. Enter your text prompt
2. Choose which model type to use (base/instruct/finetuned)

##  Results

The tool will display:
- Model summary
- Generated response
- Token usage statistics
- Visualization of token consumption

For a detailed comparison of model outputs across different prompts, see [comparisons.md](comparisons.md).


