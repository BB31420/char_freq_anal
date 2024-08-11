import nltk
from collections import defaultdict
from nltk.corpus import words

# Download the words corpus if not already downloaded
nltk.download('words')

# Load the list of valid words
word_list = [word.lower() for word in words.words()]

# Create a function to generate a pattern from the ciphered word
def generate_pattern(word):
    pattern = []
    letter_map = {}
    current_index = 0
    
    for letter in word:
        if letter not in letter_map:
            letter_map[letter] = current_index
            current_index += 1
        pattern.append(letter_map[letter])
    
    return pattern

# Check if a candidate word matches the pattern of the ciphered word
def matches_pattern(ciphered_word, candidate_word):
    if len(ciphered_word) != len(candidate_word):
        return False
    
    return generate_pattern(ciphered_word) == generate_pattern(candidate_word)

# Find all words that match the pattern of the ciphered word
def find_matching_words(ciphered_word, word_list):
    return [word for word in word_list if matches_pattern(ciphered_word, word)]

# Ask the user to provide the ciphered word
ciphered_word = input("Enter the ciphered word: ").lower()

# Get the matching words
matching_words = find_matching_words(ciphered_word, word_list)

# Specify the output file
output_file = "matching_words.txt"

# Write the matching words to a text file
with open(output_file, 'w') as file:
    if matching_words:
        file.write(f"Possible word solutions for '{ciphered_word}':\n")
        for word in matching_words:
            file.write(word + "\n")
        print(f"Matching words have been written to {output_file}.")
    else:
        file.write(f"No matching words found for '{ciphered_word}'.\n")
        print(f"No matching words found. An empty result was written to {output_file}.")

# The matching words can be returned if needed
def get_matching_words(ciphered_word):
    return find_matching_words(ciphered_word, word_list)
