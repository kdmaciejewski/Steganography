import json
import os

story_path = "./story.txt"
synonyms_path = "./synonyms.json"
output_path = "./result.txt"

# Input password
password = input("Enter password: ")

# Convert password to binary
binary_password = ''.join(format(ord(character), '08b') for character in password)
binary_index = 0  # Keeps track of which binary digit to use

# Load synonyms from JSON file
with open(synonyms_path, 'r') as f:
    synonyms = json.load(f)

# Load story from text file
with open(story_path, 'r') as f:
    story = f.read()


def replace_with_synonyms(text, synonyms_dict, binary_password):
    global binary_index
    words = text.split()
    replaced_words = []
    signature = ''

    for word in words:
        clean_word = word.strip(",.!?")  # Remove punctuation to find clean word
        if clean_word in synonyms_dict:
            synonym_list = synonyms_dict[clean_word]
            if binary_index < len(binary_password):
                # Choose synonym based on current binary digit
                binary_digit = binary_password[binary_index]
                binary_index += 1
                synonym_index = int(binary_digit)  # 0 or 1
            else:
                # If we've run out of binary digits, wrap around
                binary_index = 0
                binary_digit = binary_password[binary_index]
                synonym_index = int(binary_digit)

            # Fallback if synonym index is out of range
            if synonym_index >= len(synonym_list):
                synonym_index = 0  # Default to the first synonym

            synonym = synonym_list[synonym_index]
            signature += str(synonym_index)

            # Preserve capitalization
            if clean_word.istitle():
                synonym = synonym.capitalize()

            replaced_word = word.replace(clean_word, synonym)
            replaced_words.append(replaced_word)
        else:
            replaced_words.append(word)

    print(f"Signature: {signature}")
    return " ".join(replaced_words)


# Replace words in the story
modified_story = replace_with_synonyms(story, synonyms, binary_password)

# Save the modified story
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    f.write(modified_story)

print(f"Modified story saved to {output_path}")