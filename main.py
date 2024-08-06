import matplotlib.pyplot as plt
from collections import Counter
import string

def character_frequency(text):
    # Normalize the text to uppercase and remove non-alphabetic characters
    text = ''.join(filter(str.isalpha, text.upper()))
    
    # Count the frequency of each character in the text
    freq_counter = Counter(text)
    
    # Create a frequency dictionary with all alphabet letters
    freq_dict = {letter: 0 for letter in string.ascii_uppercase}
    freq_dict.update(freq_counter)
    
    return freq_dict

def plot_frequencies(text_freq, standard_freq, title):
    letters = list(string.ascii_uppercase)
    
    # Values for the input text
    text_values = [text_freq[letter] for letter in letters]
    
    # Values for the standard English frequency
    standard_values = [standard_freq[letter] for letter in letters]
    
    x = range(len(letters))
    
    plt.figure(figsize=(12, 6))
    
    plt.bar(x, text_values, width=0.4, label='Text Frequency', align='center')
    plt.bar(x, standard_values, width=0.4, label='Standard Frequency', align='edge')
    
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.xticks(x, letters)
    plt.legend()
    
    plt.show()

# Standard letter frequency distribution in English (percentage)
standard_letter_frequency = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70,
    'F': 2.23, 'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15,
    'K': 0.77, 'L': 4.03, 'M': 2.41, 'N': 6.75, 'O': 7.51,
    'P': 1.93, 'Q': 0.10, 'R': 5.99, 'S': 6.33, 'T': 9.06,
    'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15, 'Y': 1.97,
    'Z': 0.07
}

def get_multiple_strings():
    strings = []
    print("Enter strings (type 'done' when finished):")
    while True:
        s = input().strip()
        if s.lower() == 'done':
            break
        if s:  # Skip empty strings
            strings.append(s)
    return strings

# Example usage
strings = get_multiple_strings()
for i, text in enumerate(strings):
    text_freq = character_frequency(text)
    plot_frequencies(text_freq, standard_letter_frequency, f"Character Frequency Comparison for String {i+1}")
