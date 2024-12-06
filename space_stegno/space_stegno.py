def encode_message(file_path, secret_message, output_file_path):
    """
    Encodes a secret message into the spaces of a text file.

    :param file_path: Path to the original text file.
    :param secret_message: The secret message to encode.
    :param output_file_path: Path to save the text file with the encoded message.
    """
    # Read the original text from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    # Convert the secret message into binary format
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)

    # Encode the binary message into spaces (1 -> two spaces, 0 -> one space)
    encoded_spaces = ''.join('  ' if bit == '1' else ' ' for bit in binary_message)

    # Combine the original text with the encoded spaces
    encoded_text = original_text.replace(' ', '', len(encoded_spaces)) + encoded_spaces

    # Save the encoded text to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(encoded_text)


def decode_message(file_path):
    """
    Decodes a secret message from the spaces of a text file.

    :param file_path: Path to the text file with the encoded message.
    :return: The decoded secret message.
    """
    # Read the encoded text from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        encoded_text = file.read()

    # Extract the trailing spaces used for encoding
    trailing_spaces = encoded_text.splitlines()[-1]

    # Interpret spaces as binary (two spaces -> '1', one space -> '0')
    binary_message = ''.join('1' if char == '  ' else '0' for char in trailing_spaces.split(' '))

    # Convert binary string to the secret message
    secret_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

    return secret_message


# Example usage:
original_file = 'child_story.txt'  # Path to the file with the original text
encoded_file = 'encoded.txt'  # Path to save the file with the encoded message
secret = "HiddenMessage"

# Write original text for testing
with open(original_file, 'w', encoding='utf-8') as file:
    file.write("This is a simple text file for encoding a secret message.")

# Encode the secret message into the file
encode_message(original_file, secret, encoded_file)
print(f"Secret message encoded into '{encoded_file}'.")

# Decode the secret message from the file
decoded_message = decode_message(encoded_file)
print("Decoded message:", decoded_message)
