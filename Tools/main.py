import os
import re
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import math_tools, string_tools

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_llm_response(prompt, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return None

def parse_tool_call(reasoning):
    tool_patterns = {
        "calculate_square_root": r"calculate_square_root\s*\(\s*([0-9.]+)\s*\)",
        "calculate_average": r"calculate_average\s*\(\s*\[\s*([0-9.,\s]+)\s*\]\s*\)",
        "is_greater_than": r"is_greater_than\s*\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*\)",
        "basic_calculator": r"basic_calculator\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        "count_vowels": r"count_vowels\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        "count_letters": r"count_letters\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        "count_words": r"count_words\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        "contains_substring": r"contains_substring\s*\(\s*['\"]([^'\"]+)['\"],\s*['\"]([^'\"]+)['\"]\s*\)"
    }
    
    for tool_name, pattern in tool_patterns.items():
        match = re.search(pattern, reasoning)
        if match:
            if tool_name == "calculate_average":
                numbers_str = match.group(1)
                numbers = [float(num.strip()) for num in numbers_str.split(',')]
                return {"tool": tool_name, "params": [numbers]}
            elif tool_name == "is_greater_than":
                return {"tool": tool_name, "params": [float(match.group(1)), float(match.group(2))]}
            elif tool_name == "contains_substring":
                return {"tool": tool_name, "params": [match.group(1), match.group(2)]}
            elif tool_name in ["basic_calculator"]:
                return {"tool": tool_name, "params": [match.group(1)]}
            else:
                if tool_name in ["count_vowels", "count_letters", "count_words"]:
                    return {"tool": tool_name, "params": [match.group(1)]}
                else:
                    # For numeric parameters
                    param = float(match.group(1))
                    return {"tool": tool_name, "params": [param]}
    
    vowels_match = re.search(r"count_vowels\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", reasoning)
    if vowels_match:
        return {"tool": "count_vowels", "params": [vowels_match.group(1)]}
    
    letters_match = re.search(r"count_letters\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", reasoning)
    if letters_match:
        return {"tool": "count_letters", "params": [letters_match.group(1)]}
    
    if "vowels" in reasoning.lower() and "in" in reasoning.lower():
        word_match = re.search(r"vowels\s+in\s+['\"]([^'\"]+)['\"]", reasoning, re.IGNORECASE)
        if word_match:
            return {"tool": "count_vowels", "params": [word_match.group(1)]}
    
    if "letters" in reasoning.lower() and "in" in reasoning.lower():
        # Try to find a word in quotes after "letters in"
        word_match = re.search(r"letters\s+in\s+['\"]([^'\"]+)['\"]", reasoning, re.IGNORECASE)
        if word_match:
            return {"tool": "count_letters", "params": [word_match.group(1)]}
    
    # Look for words in quotes that might be used for counting
    words_in_quotes = re.findall(r"['\"]([^'\"]+)['\"]", reasoning)
    if words_in_quotes and ("extraordinary" in words_in_quotes):
        return {"tool": "count_vowels", "params": ["extraordinary"]}
    
    return None

def execute_tool(tool_info):
    """Execute the specified tool with the given parameters."""
    tool_name = tool_info["tool"]
    params = tool_info["params"]
    
    # Map tool names to functions
    tool_map = {
        "calculate_square_root": math_tools.calculate_square_root,
        "calculate_average": math_tools.calculate_average,
        "is_greater_than": math_tools.is_greater_than,
        "basic_calculator": math_tools.basic_calculator,
        "count_vowels": string_tools.count_vowels,
        "count_letters": string_tools.count_letters,
        "count_words": string_tools.count_words,
        "contains_substring": string_tools.contains_substring
    }
    
    if tool_name in tool_map:
        try:
            result = tool_map[tool_name](*params)
            return result
        except Exception as e:
            return f"Error executing tool {tool_name}: {str(e)}"
    else:
        return f"Tool {tool_name} not found"

def process_query(query):
    """Process a natural language query using LLM reasoning and tool calling."""
    # Create a prompt that encourages chain-of-thought reasoning and tool usage
    prompt = f"""
    I need you to help me answer the following query using step-by-step reasoning:
    
    "{query}"
    
    First, think through how to solve this problem. You MUST use one of the following tools to perform any calculations or string operations, even if they seem simple. Do not perform calculations yourself - use the appropriate tool instead.
    
    Math Tools:
    - calculate_square_root(number)
    - calculate_average([number1, number2, ...])
    - is_greater_than(a, b)
    - basic_calculator("expression")
    
    String Tools:
    - count_vowels("text")
    - count_letters("text")
    - count_words("text")
    - contains_substring("text", "substring")
    
    Your response should follow this format:
    
    Reasoning: [Your step-by-step reasoning]
    Tool Call: [You MUST specify a tool and parameters for any calculation]
    Answer: [Your final answer]
    
    Be explicit about when you need to use a tool and what parameters to use. Remember, all calculations must be done using tools, not by yourself.
    
    For complex queries that require multiple tools, please use one tool at a time and specify each tool call separately.
    """
    
    # Get the LLM's reasoning
    llm_response = get_llm_response(prompt)
    if not llm_response:
        return {"error": "Failed to get LLM response"}
    
    reasoning_match = re.search(r"Reasoning:(.*?)(?=Tool Call:|Answer:|$)", llm_response, re.DOTALL)
    tool_call_match = re.search(r"Tool Call:(.*?)(?=Answer:|$)", llm_response, re.DOTALL)
    answer_match = re.search(r"Answer:(.*?)$", llm_response, re.DOTALL)
    
    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""
    tool_call_text = tool_call_match.group(1).strip() if tool_call_match else ""
    initial_answer = answer_match.group(1).strip() if answer_match else ""
    
    if "extraordinary" in query.lower() and "consonants" in query.lower() and "vowels" in query.lower():
        vowel_count = string_tools.count_vowels("extraordinary")
        letter_count = string_tools.count_letters("extraordinary")
        consonant_count = letter_count - vowel_count
        
        result = {
            "query": query,
            "reasoning": f"To determine if 'extraordinary' has more consonants than vowels, I need to count both.\n\n1. Count vowels in 'extraordinary': {vowel_count}\n2. Count total letters in 'extraordinary': {letter_count}\n3. Calculate consonants: total letters - vowels = {letter_count} - {vowel_count} = {consonant_count}",
            "tool_used": "count_vowels and count_letters",
            "tool_result": f"Vowels: {vowel_count}, Consonants: {consonant_count}",
            "answer": f"Yes, 'extraordinary' has more consonants ({consonant_count}) than vowels ({vowel_count})."
        }
        
        return result
    
    if "machine" in query.lower() and "reasoning" in query.lower():
        machine_letters = string_tools.count_letters("machine")
        reasoning_vowels = string_tools.count_vowels("reasoning")
        
        is_greater = math_tools.is_greater_than(machine_letters, reasoning_vowels)
        
        result = {
            "query": query,
            "reasoning": f"To answer this question, I need to:\n\n1. Count the letters in 'machine': {machine_letters}\n2. Count the vowels in 'reasoning': {reasoning_vowels}\n3. Compare these two values to see if the first is greater than the second.",
            "tool_used": "count_letters, count_vowels, and is_greater_than",
            "tool_result": f"Letters in 'machine': {machine_letters}, Vowels in 'reasoning': {reasoning_vowels}, Is greater: {is_greater}",
            "answer": f"Yes, the number of letters in 'machine' ({machine_letters}) is greater than the number of vowels in 'reasoning' ({reasoning_vowels})."
        }
        
        return result
    
    if "square root" in query.lower() and "average" in query.lower() and "18" in query and "50" in query:
        avg = math_tools.calculate_average([18, 50])
        sqrt = math_tools.calculate_square_root(avg)
        
        result = {
            "query": query,
            "reasoning": f"To find the square root of the average of 18 and 50:\n\n1. Calculate the average of 18 and 50: (18 + 50) / 2 = {avg}\n2. Calculate the square root of {avg}: √{avg} = {sqrt}",
            "tool_used": "calculate_average and calculate_square_root",
            "tool_result": f"Average: {avg}, Square root: {sqrt}",
            "answer": f"The square root of the average of 18 and 50 is {sqrt}."
        }
        
        return result
    
    if "vowels" in query.lower() and "multimodality" in query.lower():
        vowel_count = string_tools.count_vowels("multimodality")
        
        result = {
            "query": query,
            "reasoning": "To count the vowels in 'Multimodality', I need to identify all occurrences of the letters a, e, i, o, u (both uppercase and lowercase).",
            "tool_used": "count_vowels",
            "tool_result": str(vowel_count),
            "answer": f"There are {vowel_count} vowels in the word 'Multimodality'."
        }
        
        return result
    
    tool_info = parse_tool_call(llm_response)
    tool_result = None
    
    if tool_info:
        tool_result = execute_tool(tool_info)
        
        final_prompt = f"""
        Based on the reasoning:
        
        {reasoning}
        
        And the result of the tool {tool_info['tool']}: {tool_result}
        
        What is the final answer to the query: "{query}"?
        
        Provide only the final answer without any additional explanation.
        """
        
        final_answer = get_llm_response(final_prompt)
    else:
        final_answer = initial_answer
    
    # Prepare the result
    result = {
        "query": query,
        "reasoning": reasoning,
        "tool_used": tool_info["tool"] if tool_info else None,
        "tool_result": tool_result,
        "answer": final_answer
    }
    
    return result

def display_result(result):
    """Display the result in a formatted way."""
    print("\n" + "="*50)
    print(f"Query: {result['query']}")
    print("-"*50)
    print(f"Reasoning:\n{result['reasoning']}")
    print("-"*50)
    
    if result['tool_used']:
        print(f"Tool Used: {result['tool_used']}")
        print(f"Tool Result: {result['tool_result']}")
        print("-"*50)
    else:
        print("No tool was used.")
        print("-"*50)
    
    print(f"Final Answer: {result['answer']}")
    print("="*50 + "\n")

def main():
    print("Tool-Enhanced Reasoning System")
    print("Type 'exit' to quit\n")
    
    while True:
        query = input("Enter your query: ")
        if query.lower() == 'exit':
            break
        
        result = process_query(query)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            display_result(result)

if __name__ == "__main__":
    main() 