import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Ładowanie modelu GPT-2 i tokenizera
model_name = "gpt2"  # Można użyć "EleutherAI/gpt-neo-1.3B" dla lepszego modelu
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

HOMOGLYPHS = {
    # Cyrylica (małe litery)
    'a': 'а',  # Cyrylica 'a'
    'e': 'е',  # Cyrylica 'e'
    'o': 'о',  # Cyrylica 'o'
    'p': 'р',  # Cyrylica 'p'
    'c': 'с',  # Cyrylica 'c'
    'x': 'х',  # Cyrylica 'x'
    'y': 'у',  # Cyrylica 'y'

    # Grecki (wielkie litery)
    'A': 'Α',  # Grecka 'A'
    'B': 'Β',  # Grecka 'B'
    'E': 'Ε',  # Grecka 'E'
    'H': 'Η',  # Grecka 'H'
    'I': 'Ι',  # Grecka 'I'
    'K': 'Κ',  # Grecka 'K'
    'M': 'Μ',  # Grecka 'M'
    'N': 'Ν',  # Grecka 'N'
    'O': 'Ο',  # Grecka 'O'
    'P': 'Ρ',  # Grecka 'P'
    'T': 'Τ',  # Grecka 'T'
    'X': 'Χ',  # Grecka 'X'
    'Y': 'Υ',  # Grecka 'Y'

    # Cyrylica (wielkie litery) 
    'C': 'С',  # Cyrylica 'C'
}

# Generowanie odwrotnej mapy
REVERSE_HOMOGLYPHS = {v: k for k, v in HOMOGLYPHS.items()}

# Funkcja generująca sensowną kontynuację tekstu
def generate_continuation_with_gpt2(previous_text, max_length=150):
    """
    Generuje sensowną kontynuację tekstu za pomocą modelu GPT-2.
    """
    # Tokenizacja poprzedniego tekstu
    input_ids = tokenizer.encode(previous_text, return_tensors='pt')

    # Tworzenie maski uwagi (wszystkie tokeny mają wartość 1, bo nie używamy paddingu)
    attention_mask = torch.ones(input_ids.shape, device=input_ids.device)

    # Generowanie kontynuacji z uwzględnieniem maski uwagi
    output = model.generate(input_ids, attention_mask=attention_mask, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2, temperature=0.7, do_sample=True, pad_token_id=50256)

    # Dekodowanie wyników
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Funkcja kodująca wiadomość
def encode_message(text, message):
    """
    Koduje wiadomość w tekście, zamieniając litery na homoglifowe odpowiedniki.
    """
    # Konwersja wiadomości na ciąg binarny
    message_binary = ''.join(format(ord(ch), '08b') for ch in message)

    # Liczba dostępnych homoglifów w tekście
    available_homoglyphs = sum(1 for char in text if char in HOMOGLYPHS)
    needed_homoglyphs = len(message_binary)

    # Sprawdzenie, czy wystarczy znaków do zakodowania
    if needed_homoglyphs > available_homoglyphs:
        print(f"W tekście jest za mało homoglifów: {available_homoglyphs}/{needed_homoglyphs}. Generowanie nowego tekstu.")
        text = generate_continuation_with_gpt2(text)  # Generowanie kontynuacji historii
        print(f"---------------\nNowy tekst:\n{text}\n----------------------\n")
    else:
        print(f"W tekście jest za wystarczająco homoglifów: {available_homoglyphs}/{needed_homoglyphs}.")
    encoded_text = []
    message_index = 0

    for char in text:
        if message_index < len(message_binary) and char in HOMOGLYPHS:
            # Zamieniamy na homoglif, jeśli bit wiadomości to 1
            if message_binary[message_index] == '1':
                encoded_text.append(HOMOGLYPHS[char])
            else:
                encoded_text.append(char)
            message_index += 1
        else:
            encoded_text.append(char)
    
    return ''.join(encoded_text)

def decode_message(encoded_text):
    """
    Dekoduje wiadomość z zakodowanego tekstu.
    """
    binary_message = []
    
    for char in encoded_text:
        if char in REVERSE_HOMOGLYPHS:
            binary_message.append('1')
        elif char in HOMOGLYPHS:
            binary_message.append('0')
    
    # Debug: Wyświetl binarną wiadomość
    # print(f"Odczytana wiadomość binarna: {''.join(binary_message)}")
    
    # Grupujemy po 8 bitów (jeden znak w ASCII) i konwertujemy na tekst
    message_chars = [
        chr(int(''.join(binary_message[i:i+8]), 2))
        for i in range(0, len(binary_message), 8)
    ]
    return ''.join(message_chars)

original_text = "Once upon a time, there was a brave hero named Alex."
hidden_message = "Ela z mlotkiem w Dubaju" # mniej więcej maksymalna długośc wiadomości
# hidden_message = "Hi" 
try:
    # Kodowanie
    encoded_text = encode_message(original_text, hidden_message)
    print("Zakodowany tekst:", encoded_text)

    # Dekodowanie
    decoded_message = decode_message(encoded_text)
    print("Odkodowana wiadomość:", decoded_message)
except ValueError as e:
    print(f"Błąd: {e}")