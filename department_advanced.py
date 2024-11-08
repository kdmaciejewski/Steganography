from faker import Faker
import random

# Initialize Faker
fake = Faker()


# Function to determine bit based on first letter
def letter_to_bit(letter):
    vowels = "AEIOU"
    return '0' if letter.upper() in vowels else '1'


# Function to encode a single byte as a department
def generate_department(byte):
    department = []
    bits = f"{byte:08b}"  # Convert byte to 8-bit binary string

    for i in range(0, 8, 4):  # Each person now contributes 4 bits
        # Generate random names until we get one with the right first-letter bits
        while True:
            name = fake.first_name()
            surname = fake.last_name()
            middle_name = fake.first_name() if random.choice([True, False]) else ""
            suffix = random.choice(["Jr", "Sr"]) if random.choice([True, False]) else ""

            # Generate the 4-bit code based on the person's attributes
            name_bit = letter_to_bit(name[0])  # Bit 1: First letter of name
            surname_bit = letter_to_bit(surname[0])  # Bit 2: First letter of surname
            middle_bit = '1' if middle_name else '0'  # Bit 3: Middle name existence
            suffix_bit = '1' if suffix else '0'  # Bit 4: Suffix existence

            # Check if this 4-bit code matches the desired bits
            if name_bit == bits[i] and surname_bit == bits[i + 1] and middle_bit == bits[i + 2] and suffix_bit == bits[
                i + 3]:
                department.append((name, middle_name, surname, suffix))
                break

    return department


# Function to encode a message into departments
def encode_message(message):
    byte_array = message.encode('utf-8')  # Encode message to bytes
    departments = []

    for byte in byte_array:
        department = generate_department(byte)
        departments.append(department)

    return departments


# Function to decode the message from departments
def decode_message(departments):
    bytes_list = []

    for department in departments:
        bits = ""
        for name, middle_name, surname, suffix in department:
            # Extract bits from the name, surname, middle name, and suffix
            name_bit = letter_to_bit(name[0])
            surname_bit = letter_to_bit(surname[0])
            middle_bit = '1' if middle_name else '0'
            suffix_bit = '1' if suffix else '0'
            bits += name_bit + surname_bit + middle_bit + suffix_bit

        # Convert 8 bits to a byte and append to the list
        byte = int(bits, 2)
        bytes_list.append(byte)

    # Convert the list of bytes back to the original string
    decoded_message = bytes(bytes_list).decode('utf-8')
    return decoded_message


if __name__ == "__main__":

    secret_message = "Hi"
    encoded_departments = encode_message(secret_message)

    print("Encoded Departments:")
    for i, department in enumerate(encoded_departments):
        print(f"Department {i + 1}:")
        for name, middle_name, surname, suffix in department:
            middle = f" {middle_name}" if middle_name else ""
            suff = f" {suffix}" if suffix else ""
            print(f"  - {name}{middle} {surname}{suff}")

    # Decode the message
    decoded_message = decode_message(encoded_departments)
    print("\nDecoded Message:", decoded_message)
