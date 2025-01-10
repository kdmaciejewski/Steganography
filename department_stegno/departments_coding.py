from faker import Faker

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

    for i in range(0, 8, 2):  # Each person contributes 2 bits
        # Generate random names until we get one with the right first-letter bits
        while True:
            name = fake.first_name()
            surname = fake.last_name()
            name_bit = letter_to_bit(name[0])
            surname_bit = letter_to_bit(surname[0])

            if name_bit == bits[i] and surname_bit == bits[i + 1]:
                department.append((name, surname))
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
        for name, surname in department:
            # Extract bits from the first letters of name and surname
            name_bit = letter_to_bit(name[0])
            surname_bit = letter_to_bit(surname[0])
            bits += name_bit + surname_bit

        # Convert 8 bits to a byte and append to the list
        byte = int(bits, 2)
        bytes_list.append(byte)

    # Convert the list of bytes back to the original string
    decoded_message = bytes(bytes_list).decode('utf-8')
    return decoded_message


if __name__ == "__main__":
    secret_message = "Hello"
    encoded_departments = encode_message(secret_message)

    print("Encoded Departments:")
    for i, department in enumerate(encoded_departments):
        print(f"Department {i + 1}:")
        for name, surname in department:
            print(f"  - {name} {surname}")

    # Decode the message
    decoded_message = decode_message(encoded_departments)
    print("\nDecoded Message:", decoded_message)
