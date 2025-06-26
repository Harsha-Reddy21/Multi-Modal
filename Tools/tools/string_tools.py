def count_vowels(text):
    vowels = "aeiouAEIOU"
    return sum(1 for char in text if char in vowels)

def count_letters(text):
    return sum(1 for char in text if char.isalpha())

def count_words(text):
    return len(text.split())

def contains_substring(text, substring):
    return substring.lower() in text.lower() 