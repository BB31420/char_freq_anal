import matplotlib.pyplot as plt
plt.ion()  # Turn on interactive mode
from collections import Counter
import string
import numpy as np
from scipy.stats import chisquare
import math

def character_frequency(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    freq_counter = Counter(text)
    freq_dict = {letter: 0 for letter in string.ascii_uppercase}
    freq_dict.update(freq_counter)
    return freq_dict

def plot_frequencies(text_freq, standard_freq, title):
    letters = list(string.ascii_uppercase)
    text_values = [text_freq[letter] for letter in letters]
    standard_values = [standard_freq[letter] for letter in letters]
    x = range(len(letters))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x, text_values, width=0.4, label='Text Frequency', align='center')
    ax.bar(x, standard_values, width=0.4, label='Standard Frequency', align='edge')
    ax.set_xlabel('Letters')
    ax.set_ylabel('Frequency')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(letters)
    ax.legend()
    fig.canvas.draw()
    fig.canvas.flush_events()

def calculate_ioc(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    n = len(text)
    freqs = Counter(text)
    ioc = sum([freq * (freq - 1) for freq in freqs.values()]) / (n * (n - 1))
    return ioc

def calculate_chi_square(observed_freq, expected_freq):
    observed = np.array(list(observed_freq.values()))
    expected = np.array(list(expected_freq.values()))
    chi2, p_value = chisquare(observed, expected)
    return chi2, p_value

def analyze_ngrams(text, n):
    text = ''.join(filter(str.isalpha, text.upper()))
    ngrams = [text[i:i+n] for i in range(len(text)-n+1)]
    return Counter(ngrams).most_common(10)

def get_multiple_strings():
    strings = []
    print("Enter strings (type 'done' when finished):")
    while True:
        s = input().strip()
        if s.lower() == 'done':
            break
        if s:
            strings.append(s)
    return strings

def normalize_frequency(freq_dict):
    total = sum(freq_dict.values())
    return {k: (v / total) * 100 for k, v in freq_dict.items()}

def rank_frequency(freq_dict):
    return sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)

def vowel_consonant_ratio(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    vowels = sum(text.count(v) for v in 'AEIOU')
    return vowels / len(text)

def find_repeated_sequences(text, min_length=3, max_length=5):
    text = ''.join(filter(str.isalpha, text.upper()))
    sequences = {}
    for length in range(min_length, max_length + 1):
        for i in range(len(text) - length + 1):
            seq = text[i:i+length]
            if seq in sequences:
                sequences[seq].append(i)
            else:
                sequences[seq] = [i]
    return {k: v for k, v in sequences.items() if len(v) > 1}

def calculate_ioc_substrings(text, max_length=10):
    text = ''.join(filter(str.isalpha, text.upper()))
    iocs = []
    for length in range(1, max_length + 1):
        substrings = [text[i::length] for i in range(length)]
        iocs.append(np.mean([calculate_ioc(s) for s in substrings]))
    return iocs

def calculate_entropy(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    freq = Counter(text)
    entropy = 0
    for count in freq.values():
        p = count / len(text)
        entropy -= p * math.log2(p)
    return entropy

def frequency_analysis_solver(ciphertext):
    english_freq_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    cipher_freq = Counter(filter(str.isalpha, ciphertext.upper()))
    sorted_cipher_freq = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
    mapping = {}
    for (cipher_char, _), plain_char in zip(sorted_cipher_freq, english_freq_order):
        mapping[cipher_char] = plain_char
    plaintext = ''.join(mapping.get(c.upper(), c) for c in ciphertext)
    return plaintext, mapping

def get_unused_letters(mapping):
    used_plain = set(mapping.values())
    return [letter for letter in string.ascii_uppercase if letter not in used_plain]

def get_next_likely_letter(freq_order, used_letters):
    for letter in freq_order:
        if letter not in used_letters:
            return letter
    return None  # This should never happen if freq_order contains all letters

def update_mapping(mapping, cipher_freq_order, english_freq_order):
    used_plain = set(mapping.values())
    for cipher_letter in cipher_freq_order:
        if cipher_letter not in mapping:
            next_plain = get_next_likely_letter(english_freq_order, used_plain)
            if next_plain:
                mapping[cipher_letter] = next_plain
                used_plain.add(next_plain)
    return mapping

def refine_mapping(ciphertext, initial_mapping):
    english_freq_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    cipher_freq = Counter(filter(str.isalpha, ciphertext.upper()))
    cipher_freq_order = [letter for letter, _ in cipher_freq.most_common()]
    
    current_mapping = initial_mapping.copy()
    
    while True:
        print("\nCurrent decryption:")
        print(''.join(current_mapping.get(c.upper(), c) for c in ciphertext))
        print("\nCurrent mapping:")
        for cipher, plain in current_mapping.items():
            print(f"{cipher} -> {plain}")
        
        change = input("\nEnter a change (e.g., 'A:B' to map A to B), or 'done' to finish: ")
        if change.lower() == 'done':
            break
        if ':' in change:
            cipher, plain = change.split(':')
            cipher, plain = cipher.upper(), plain.upper()
            
            # Remove the old mapping if it exists
            if cipher in current_mapping:
                del current_mapping[cipher]
            
            # Remove the new plain letter from any existing mappings
            for key in list(current_mapping.keys()):
                if current_mapping[key] == plain:
                    del current_mapping[key]
            
            # Add the new mapping
            current_mapping[cipher] = plain
            
            # Update the rest of the mapping
            current_mapping = update_mapping(current_mapping, cipher_freq_order, english_freq_order)
    
    return current_mapping

def solve_substitution_cipher(ciphertext):
    plaintext, initial_mapping = frequency_analysis_solver(ciphertext)
    print("Initial decryption attempt:")
    print(plaintext)
    
    final_mapping = refine_mapping(ciphertext, initial_mapping)
    
    final_plaintext = ''.join(final_mapping.get(c.upper(), c) for c in ciphertext)
    return final_plaintext, final_mapping

# Standard letter frequency distribution in English (percentage)
standard_letter_frequency = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70,
    'F': 2.23, 'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15,
    'K': 0.77, 'L': 4.03, 'M': 2.41, 'N': 6.75, 'O': 7.51,
    'P': 1.93, 'Q': 0.10, 'R': 5.99, 'S': 6.33, 'T': 9.06,
    'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15, 'Y': 1.97,
    'Z': 0.07
}

# Main execution
if __name__ == "__main__":
    strings = get_multiple_strings()
    for i, text in enumerate(strings):
        print(f"\nAnalysis for String {i+1}:")
        
        # Character frequency analysis
        text_freq = character_frequency(text)
        normalized_text_freq = normalize_frequency(text_freq)
        plot_frequencies(normalized_text_freq, standard_letter_frequency, f"Character Frequency Comparison for String {i+1}")
        
        # Index of Coincidence
        ioc = calculate_ioc(text)
        print(f"Index of Coincidence: {ioc:.4f}")
        
        # Chi-Square Test
        try:
            chi2, p_value = calculate_chi_square(normalized_text_freq, standard_letter_frequency)
            print(f"Chi-Square Statistic: {chi2:.4f}")
            print(f"p-value: {p_value:.4f}")
        except Exception as e:
            print(f"Error in Chi-Square calculation: {e}")
        
        # N-gram analysis
        print("\nTop 10 bigrams:")
        print(analyze_ngrams(text, 2))
        print("\nTop 10 trigrams:")
        print(analyze_ngrams(text, 3))
        
        # Letter Frequency Ranking
        print("\nLetter Frequency Ranking:")
        print(rank_frequency(text_freq)[:10])  # Top 10 most frequent letters
        
        # Vowel to Consonant Ratio
        print(f"\nVowel to Text Ratio: {vowel_consonant_ratio(text):.4f}")
        
        # Repeated Sequences
        print("\nRepeated Sequences:")
        repeated = find_repeated_sequences(text)
        for seq, positions in repeated.items():
            print(f"{seq}: {positions}")
        
        # IoC for Substrings
        print("\nIoC for Substrings:")
        iocs = calculate_ioc_substrings(text)
        fig, ax = plt.subplots()
        ax.plot(range(1, len(iocs) + 1), iocs)
        ax.set_title("IoC for Substrings of Different Lengths")
        ax.set_xlabel("Substring Length")
        ax.set_ylabel("Index of Coincidence")
        fig.canvas.draw()
        fig.canvas.flush_events()
        
        # Shannon Entropy
        print(f"\nShannon Entropy: {calculate_entropy(text):.4f}")
        
        # Attempt to solve the cipher
        print("\nAttempting to solve the cipher...")
        plaintext, mapping = solve_substitution_cipher(text)
        print("\nFinal decryption:")
        print(plaintext)
        print("\nFinal mapping:")
        for cipher, plain in mapping.items():
            print(f"{cipher} -> {plain}")

    plt.show(block=True)  # Keep the script running and plots open