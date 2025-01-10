import pandas as pd
from faker import Faker

if __name__ == "__main__":# This program adds two numbers

    # Tworzenie generatora losowych danych
    fake = Faker('pl_PL')  # 'pl_PL' generuje polskie imiona i nazwiska

    # Generowanie listy słowników z imionami i nazwiskami
    data = [{'Imię': fake.first_name(), 'Nazwisko': fake.last_name()} for _ in range(1000)]

    # Tworzenie DataFrame
    df = pd.DataFrame(data)

    # Zapisanie DataFrame do pliku CSV
    df.to_csv('dane.csv', index=False, encoding='utf-8')

    print("Dane zostały zapisane do pliku dane.csv.")

