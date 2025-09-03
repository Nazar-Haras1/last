import deepl
import requests
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN_ID = os.getenv("TOKEN_ID")
TOKEN = os.getenv("TOKEN")
AUTH_KEY = os.getenv("AUTH_KEY")
# ініціалізую перекладач
translator = deepl.Translator(AUTH_KEY)

# доступні мови для перекладу
languages = {
    "AR": "Арабська",
    "BG": "Болгарська",
    "CS": "Чеська",
    "DA": "Данська",
    "DE": "Німецька",
    "EL": "Грецька",
    "EN-US": "Англійська (всі варіанти англійської мови)",
    "ES": "Іспанська (всі варіанти іспанської)",
    "ET": "Естонська",
    "FI": "Фінська",
    "FR": "Французька",
    "HE": "Іврит (лише нові моделі)",
    "HU": "Угорська",
    "ID": "Індонезійська",
    "IT": "Італійська",
    "JA": "Японська",
    "KO": "Корейська",
    "LT": "Литовська",
    "LV": "Латиська",
    "NB": "Норвезький букмол",
    "NL": "Нідерландська",
    "PL": "Польська",
    "PT": "Португальська (всі варіанти)",
    "RO": "Румунська",
    "SK": "Словацька",
    "SL": "Словенська",
    "SV": "Шведська",
    "TH": "Тайська (лише нові моделі)",
    "TR": "Турецька",
    "UK": "Українська",
    "VI": "Вʼєтнамська (лише нові моделі)",
    "ZH": "Китайська (всі варіанти)"
}

# вивожу доступні мови з кодами
print("Доступні мови:")
for key, value in languages.items():
  print (f"{key}+ {value}")


# функція для отримання команди, тексту та мови від користувача
def get_command():
    # змінна для дозволеної команди
    valid_commands = "/translate"
    # цикл для отримання команди та тексту
    while True:
        user_input = input("Введіть команду та текст приклад(/translate ваш текст): ").strip()

        # перевірка якщо нічого не введено
        if not user_input:
            print("Ви нічого не ввели, спробуйте ще раз")
            continue

        # розділяю введений рядок на команду та текст для перекладу
        split_text = user_input.split(" ", 1)

        # отримаю команду
        command = split_text[0]

        # перевіряю на валідність введеня команди
        if command != valid_commands:
            print(f"Невірно введена команда: {command}")
            print(f"Дозволені команди: {valid_commands}")
            continue

        # перевіряю чи ввели текст після команди
        if len(split_text) < 2:
            print("Ви ввели лише команду, повторіть спробу")
            continue

        # отримую текст для перекладу
        text_to_translate = split_text[1]

        # цикл на перевірку валідності введення мови
        while True:
            user_input_lang = input("Введіть код мови (приклад: EN-US, DE, FR): ").strip()
            # перевіряю чи введена мова є у списку доступних мов
            if user_input_lang in languages.keys():
                # усе вірно, повертаємо дані
                print("Команда та текст вірно введені")
               # закінчую цикл на введення мови
                break
            # інакше прошу ввести мову ще раз

            else:
                print(f"Мова '{user_input_lang}' не доступна.")
                print("Доступні мови:", ", ".join(languages.keys()))
                continue
        # вихід з основного циклу після успішного вводу
        break  
    
    return command, text_to_translate, user_input_lang


# отримую команду, текст та мову від користувача
comand, text_to_translate, user_input_lang = get_command()
# роблю переклад тексту на обрану мову
result = translator.translate_text(f"{text_to_translate}", target_lang=f"{user_input_lang}")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# данні для передачи в телеграм
payload = {
    "chat_id": TOKEN_ID,
    "text": result
}
# відправляю запит в телеграм
response = requests.post(url, data=payload)
