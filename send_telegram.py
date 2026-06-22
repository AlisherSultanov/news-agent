import os
import requests
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')
with open('bulletin.txt', 'r', encoding='utf-8') as f:
    text = f.read()
parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
for part in parts:
    r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={'chat_id': '@panorama_uzb', 'text': part})
    print(r.json())
print('Otpravleno!')
