# Coding descritpion:
# Replaces 0 with a zero-width space (\u200B) and 1 with a zero-width non-joiner (\u200C).
# Concatenates the encoded message with the original text using a zero-width joiner (\u200D) as a delimiter.

# Function to hide a secret message using zero-width characters
def encrypt(plain_text, secret_message):
    # Encode the secret message using zero-width characters
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    zero_width_encoding = binary_message.replace('0', '\u200B').replace('1', '\u200C')

    # Combine plain text and encoded secret message
    encoded_text = plain_text + '\u200D' + zero_width_encoding + '\u200D'
    return encoded_text


# Function to decrypt and reveal the hidden message
def decrypt(encoded_text):
    # Split the encoded text to separate the original message from the hidden part
    if '\u200D' not in encoded_text:
        return "No hidden message found.", encoded_text

    # Extract hidden part and the original message
    plain_text, encoded_message = encoded_text.split('\u200D', 1)
    encoded_message = encoded_message.strip('\u200D')

    # Convert zero-width characters back to binary
    binary_message = encoded_message.replace('\u200B', '0').replace('\u200C', '1')

    # Convert binary to characters to reveal the hidden message
    secret_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

    return plain_text, secret_message


if __name__ == '__main__':
    # # Example usage:
    # plain_text = "Hello, how are you?"
    # secret_message = "Hidden123"
    # encoded_text = encrypt(plain_text, secret_message)
    # print(f"Encoded Text: {encoded_text}")

    encoded_text = "Hello, how are you?‍​‌​​‌​​​​‌‌​‌​​‌​‌‌​​‌​​​‌‌​​‌​​​‌‌​​‌​‌​‌‌​‌‌‌​​​‌‌​​​‌​​‌‌​​‌​​​‌‌​​‌‌‍"
    # Decrypting to reveal the hidden message
    original_text, decoded_message = decrypt(encoded_text)
    print(f"Original Text: {original_text}")
    print(f"Decoded Hidden Message: {decoded_message}")
