from dotenv import load_dotenv
import os
import anthropic
from collector import collect_news, format_for_agent

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """Sen ikki tilli yangiliklar agentisan.
Vazifang: showbiznes, kino, musiqa, bloggerlar haqida eng muhim 10 ta yangilik tayyorlash.

Har bir yangilik uchun FORMAT:
---
🔹 РУССКИЙ:
ЗАГОЛОВОК: [sarlavha rus tilida]
ПОДВОДКА: [kirish so'zi rus tilida, televideniye uslubida]
Источник: [manba]

🔹 O'ZBEK:
SARLAVHA: [sarlavha o'zbek tilida]
KIRISH SO'ZI: [kirish so'zi o'zbek tilida]
Manba: [manba]
---

Qoidalar:
1. Har bir yangilik AVVAL rus tilida, KEYIN o'zbek tilida yoz
2. Eng muhim 10 ta yangilikni tanla
3. Televideniye uslubida yoz
4. Abdukodir Xusanov, o'zbek yulduzlari, dunyo shoubiznesiga ustunlik ber"""

def generate_bulletin(news_text):
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Quyidagi yangiliklar asosida ikki tilli (rus va o'zbek) yangiliklar chiqarini tayyorla:\n\n{news_text}"}
        ]
    )
    return message.content[0].text

def main():
    print("=" * 60)
    print("SHOWBIZNES YANGILIKLAR AGENTI ISHGA TUSHDI!")
    print("=" * 60)

    print("\nYangiliklar yig'ilmoqda...")
    news_items = collect_news()
    news_text = format_for_agent(news_items)
    print(f"Jami {len(news_items)} ta yangilik topildi")

    print("\nClaude yangiliklar chiqarini tayyorlamoqda...")
    bulletin = generate_bulletin(news_text)

    print("\nTAYYOR VYPUSK:")
    print("=" * 60)
    print(bulletin)

    with open("bulletin.txt", "w", encoding="utf-8") as f:
        f.write(bulletin)
    print("\nVypusk 'bulletin.txt' fayliga saqlandi!")

if __name__ == "__main__":
    main()
