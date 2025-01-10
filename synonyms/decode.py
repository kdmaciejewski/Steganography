import json

# Paths to required files
encoded_story_path = "./result.txt"
synonyms_path = ".synonyms.json"
decoded_story_path = ".decoded_story.txt"

# Input the password
password = input("Enter password to decode: ")

# Convert the password into binary
binary_password = ''.join(format(ord(char), '08b') for char in password)
binary_index = 0  # Keeps track of the binary digit being used

# Load the synonyms dictionary
with open(synonyms_path, 'r') as f:
    synonyms = json.load(f)

# Load the encoded story
with open(encoded_story_path, 'r') as f:
    encoded_story = f.read()


def decode_story(encoded_text, synonyms_dict, binary_password):
    """
    Decodes the encoded story by reversing the synonym replacement.
    :param encoded_text: The encoded story text
    :param synonyms_dict: Dictionary mapping words to their synonyms
    :param binary_password: Binary representation of the password
    :return: Decoded original story
    """
    global binary_index
    words = encoded_text.split()
    decoded_words = []

    for word in words:
        # Remove punctuation to isolate the base word
        stripped_word = word.strip(",.!?")
        punctuation = word[len(stripped_word):] if len(word) > len(stripped_word) else ""

        # Check if the stripped word is in the synonym list
        original_word = None
        for key, synonym_list in synonyms_dict.items():
            if stripped_word in synonym_list:
                # Determine the synonym index from the binary password
                if binary_index < len(binary_password):
                    binary_digit = binary_password[binary_index]
                    binary_index += 1
                else:
                    # Wrap around binary password if it runs out
                    binary_index = 0
                    binary_digit = binary_password[binary_index]

                chosen_index = int(binary_digit)

                # If the chosen index matches the current synonym, it's the original word
                if synonym_list[chosen_index] == stripped_word:
                    original_word = key
                    break

        # If we found the original word, replace it; otherwise, leave it unchanged
        if original_word:
            if word.istitle():
                original_word = original_word.capitalize()
            decoded_word = original_word + punctuation
        else:
            decoded_word = word  # Leave word unchanged if not a synonym

        decoded_words.append(decoded_word)

    return " ".join(decoded_words)


# Decode the encoded story
decoded_story = decode_story(encoded_story, synonyms, binary_password)

# Save the decoded story
with open(decoded_story_path, 'w') as f:
    f.write(decoded_story)

print(f"Decoded story saved to {decoded_story_path}")