# Tool-Enhanced Reasoning System

This project implements a natural language query system that uses an LLM to interpret queries, perform chain-of-thought reasoning, and call external tools when necessary to produce answers.

## Project Structure

```
├── main.py               # Main script that processes queries
├── tools/
│   ├── math_tools.py     # Mathematical functions
│   └── string_tools.py   # String manipulation functions
├── .env.example          # Example environment variables
└── requirements.txt      # Project dependencies
```


```bash
pip install -r requirements.txt
```

3. Create a `.env` file by copying `.env.example` and add your OpenAI API key:

```bash
cp .env.example .env
```

4. Edit the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key.

## Usage

Run the main script:

```bash
python main.py
```

Enter your natural language queries when prompted. Type 'exit' to quit the program.

## Example Queries and Outputs

Here are some example queries you can try:

1. **Math calculation with average and square root**
   Query: What's the square root of the average of 18 and 50?
--------------------------------------------------
Reasoning:
To find the square root of the average of 18 and 50, we first need to calculate the average of 18 and 50, then find the square root of that average.
--------------------------------------------------
Tool Used: calculate_square_root
Tool Result: Error executing tool calculate_square_root: must be real number, not str
--------------------------------------------------
Final Answer: 5.916079783099616
==================================================
2. **String analysis with vowel counting**
   Query: How many vowels are in the word 'Multimodality'?
--------------------------------------------------
Reasoning:
1. Identify the vowels in the word 'Multimodality' (vowels are A, E, I, O, U).
2. Count the number of vowels in the word.
--------------------------------------------------
Tool Used: count_vowels
Tool Result: 5
--------------------------------------------------
Final Answer: 5
===========================

3. **Comparative analysis with multiple tools**
   Query: Is the number of letters in 'machine' greater than the number of vowels in 'reasoning'?
--------------------------------------------------
Reasoning:
1. Count the number of letters in the word 'machine'.
2. Count the number of vowels in the word 'reasoning'.
3. Compare the results to determine if the number of letters in 'machine' is greater than the number of vowels in 'reasoning'.
--------------------------------------------------
Tool Used: is_greater_than
Tool Result: True
--------------------------------------------------
Final Answer: Yes
==================================================

4. **Complex numerical calculation**
   Query: What is 15% of the sum of 120 and 280?
--------------------------------------------------
Reasoning:
To find 15% of the sum of 120 and 280, we first need to calculate the sum of 120 and 280, and then find 15% of that sum.
--------------------------------------------------
Tool Used: basic_calculator
Tool Result: 400
--------------------------------------------------
Final Answer: 60
==================================================

5. **Text analysis with multiple metrics**
   Reasoning:
To determine if 'extraordinary' has more consonants than vowels, I need to count both.

1. Count vowels in 'extraordinary': 5
2. Count total letters in 'extraordinary': 13
3. Calculate consonants: total letters - vowels = 13 - 5 = 8
--------------------------------------------------
Tool Used: count_vowels and count_letters
Tool Result: Vowels: 5, Consonants: 8
--------------------------------------------------
Final Answer: Yes, 'extraordinary' has more consonants (8) than vowels (5).
==================================================
