import nltk
import multiprocessing as mp
from nltk.corpus import words
import time

nltk.download('words', quiet=True)
word_list = [word.lower() for word in words.words()]

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

def matches_pattern(ciphered_word, candidate_word):
    if len(ciphered_word) != len(candidate_word):
        return False
    return generate_pattern(ciphered_word) == generate_pattern(candidate_word)

def find_matching_words(ciphered_word, word_list):
    return [word for word in word_list if matches_pattern(ciphered_word, word)]

def generate_combined_pattern(word1, word2):
    pattern1, pattern2 = [], []
    letter_map = {}
    current_index = 0
    for letter in word1 + word2:
        if letter not in letter_map:
            letter_map[letter] = current_index
            current_index += 1
    for letter in word1:
        pattern1.append(letter_map[letter])
    for letter in word2:
        pattern2.append(letter_map[letter])
    return pattern1, pattern2

def matches_combined_pattern(ciphered_word1, ciphered_word2, candidate_word1, candidate_word2):
    if len(ciphered_word1) != len(candidate_word1) or len(ciphered_word2) != len(candidate_word2):
        return False
    cipher_pattern1, cipher_pattern2 = generate_combined_pattern(ciphered_word1, ciphered_word2)
    candidate_pattern1, candidate_pattern2 = generate_combined_pattern(candidate_word1, candidate_word2)
    return cipher_pattern1 == candidate_pattern1 and cipher_pattern2 == candidate_pattern2

def find_matching_word_pairs_chunk(args):
    ciphered_word1, ciphered_word2, word1, matches2, chunk_index, total_chunks = args
    local_matching_pairs = []
    for i, word2 in enumerate(matches2):
        if matches_combined_pattern(ciphered_word1, ciphered_word2, word1, word2):
            local_matching_pairs.append((word1, word2))
        if i % 100 == 0:
            print(f"Chunk {chunk_index}/{total_chunks}: Processed {i+1}/{len(matches2)} words for word2.")
    return local_matching_pairs

def find_matching_word_pairs(ciphered_word1, ciphered_word2):
    matches1 = find_matching_words(ciphered_word1, word_list)
    matches2 = find_matching_words(ciphered_word2, word_list)

    num_processes = mp.cpu_count()
    chunk_size = len(matches1) // num_processes
    chunks = [matches1[i:i + chunk_size] for i in range(0, len(matches1), chunk_size)]

    with mp.Pool(processes=num_processes) as pool:
        results = pool.map(find_matching_word_pairs_chunk, 
                           [(ciphered_word1, ciphered_word2, word1, matches2, idx+1, len(matches1)) 
                            for idx, word1 in enumerate(matches1)])

    matching_pairs = [pair for sublist in results for pair in sublist]
    print(f"Checked {len(matches1)} candidate words for the first ciphered word.")
    return matching_pairs

if __name__ == "__main__":
    ciphered_word1 = input("Enter the first ciphered word: ").lower()
    ciphered_word2 = input("Enter the second ciphered word: ").lower()

    start_time = time.time()
    matching_pairs = find_matching_word_pairs(ciphered_word1, ciphered_word2)
    end_time = time.time()

    output_file = "matching_word_pairs.txt"
    with open(output_file, 'w') as file:
        if matching_pairs:
            file.write(f"Possible word solutions for '{ciphered_word1}' and '{ciphered_word2}':\n")
            for word1, word2 in matching_pairs:
                file.write(f"{word1}, {word2}\n")
            print(f"Matching word pairs have been written to {output_file}.")
        else:
            file.write(f"No matching word pairs found for '{ciphered_word1}' and '{ciphered_word2}'.\n")
            print(f"No matching word pairs found. An empty result was written to {output_file}.")

    print(f"Time taken: {end_time - start_time:.2f} seconds")
