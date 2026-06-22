from dotenv import load_dotenv
import os
import anthropic
import requests

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL = "@panoramauzb_bot"

SYSTEM_PROMPT = """Ты — главный редактор новостного телепроекта.
Отбирай только достоверные новости из официальных источников.
Формируй выпуск строго и профессионально.
Пиши подводки для ведущего в телевизионном стиле."""

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHANNEL, "text": text})

print("Агент главного редактора запущен!")
print("-" * 50)

while True:
    user_input = input("\nВы: ")
    if user_input.lower() == "выход":
        print("Агент остановлен.")
        break

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_input}]
    )

    result = response.content[0].text
    print(f"\nРедактор: {result}")
    print("-" * 50)

    send = input("Отправить в Telegram? (да/нет): ")
    if send.lower() == "да":
        send_to_telegram(result)
        print("✅ Отправлено в канал!")
