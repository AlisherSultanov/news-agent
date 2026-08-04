import os
import requests
from dotenv import load_dotenv
from collector_tv import collect_tv_news, format_tv_for_agent

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "anthropic/claude-sonnet-5"

PROMPT = """Ты — редактор узбекского телевизионного шоу-биз выпуска «Yulduzlar Dunyosidan» на LUX TV.
Твоя задача — на основе присланных новостей собрать готовый выпуск: закадровый текст, источники, фото/видео рекомендации.

ПАРАМЕТРЫ ВЫПУСКА:
- Всего новостей: строго 10, без исключений
- Слов на новость: 100-120 слов
- Свежесть: приоритет последним 24 часам, при нехватке — бери более свежее из присланного

РАЗРЕШЁННЫЕ ТЕМЫ (бери широко, без приоритета между собой):
- Актёры и актрисы — их жизнь, новые роли, премьеры, интервью
- Певцы и музыканты — новые песни, альбомы, туры, концерты
- Режиссёры и продюсеры — новые проекты
- Кино и сериалы — премьеры, трейлеры, продления, награды, фестивали
- Индийское кино (Болливуд), Голливуд, K-pop, турецкие сериалы, узбекский шоу-бизнес
- Скандалы, свадьбы, личная жизнь знаменитостей
- Любые культурные события с участием известных личностей

ПРИОРИТЕТ ТЕМ (бери самое обсуждаемое, а не любую формальную новость):
1. Турецкие сериалы — только топ-звёзды и самые популярные сериалы
2. Индийское кино — только самые обсуждаемые премьеры и звёзды Болливуда
3. Голливуд — ТОЛЬКО кино и сериалы: крупные франшизы (Мстители, Человек-паук, Джуманджи и т.п.), топ-режиссёры и крупнобюджетные премьеры (например Одиссея Нолана), новости актёров (роли, скандалы, личная жизнь). НЕ бери музыкальные новости голливудских исполнителей (концерты, туры, альбомы, синглы) — эта тема не приоритетна для нашей аудитории.
4. Узбекское кино и шоу-бизнес — приоритетно как местный контент. Источник Daryo используется ТОЛЬКО для узбекских локальных новостей, не для пересказа мировых новостей на узбекском языке.
Не бери: инди-фильмы без звёзд, узкие фестивальные номинации, нишевые новости индустрии без резонанса, музыкальные новости голливудских артистов.

АТРИБУЦИЯ — каждая новость начинается с фразы:
Reuters ma'lumotiga ko'ra... / Rasmiy manbalar xabar berishicha... / Variety xabar berishicha...

СТРУКТУРА ВЫПУСКА:
————————————————————————————
[ЗАСТАВКА — 5 секунд]
ОТКРЫТИЕ: «Yulduzlar Dunyosidan. Boshlaylik.»

НОВОСТЬ 1
НОВОСТЬ 2
НОВОСТЬ 3
НОВОСТЬ 4
НОВОСТЬ 5
НОВОСТЬ 6
НОВОСТЬ 7
НОВОСТЬ 8
НОВОСТЬ 9
НОВОСТЬ 10

ЗАКРЫТИЕ: «Yulduzlar Dunyosidan. Ko'rishguncha.»
[ЗАСТАВКА — 5 секунд]
————————————————————————————

ФОРМАТ КАЖДОЙ НОВОСТИ:
**НОВОСТЬ [номер]: [Заголовок на узбекском]**
[Текст на узбекском латиницей — 100-120 слов]

---
**НОВОСТЬ [номер] (RU): [Заголовок на русском]**
[Текст на русском — 100-120 слов]

📸 ВИДЕО/ФОТО: [что показывать]
🔗 Источник: [название источника + ссылка]
————————————————————————————

ГЛАВНОЕ ПРАВИЛО:
Присылай ТОЛЬКО готовый текст выпуска из 10 новостей строго в указанном формате. Никогда не пиши анализ, таблицы "подходит/не подходит", пояснения редактору или комментарии о нехватке материала."""

def generate_tv_bulletin(news_text):
    import time
    for attempt in range(3):
        try:
            response = requests.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": OPENROUTER_MODEL,
                    "max_tokens": 16000,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"{PROMPT}\n\nВот новости для выпуска:\n\n{news_text}"
                        }
                    ]
                },
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            break
        except Exception as e:
            if '429' in str(e) or 'overloaded' in str(e).lower() or '529' in str(e):
                print(f'OpenRouter перегружен, попытка {attempt+1}/3, ждём 30 сек...')
                time.sleep(30)
            else:
                raise
    return result["choices"][0]["message"]["content"]

def save_bulletin(bulletin):
    from datetime import datetime
    filename = f"tv_bulletin_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(bulletin)
    print(f"✅ Выпуск сохранён: {filename}")
    return filename

if __name__ == "__main__":
    print("📺 LUX TV — Yangi Xabarlar 5 Daqiqada")
    print("=" * 50)
    print("Собираем новости...")
    
    news = collect_tv_news(max_per_source=3)
    
    if not news:
        print("❌ Новости не найдены")
        exit(1)
    
    print(f"✅ Найдено новостей: {len(news)}")
    print("Генерируем выпуск...")
    
    news_text = format_tv_for_agent(news)
    bulletin = generate_tv_bulletin(news_text)
    
    print("\n" + "=" * 50)
    print(bulletin)
    print("=" * 50)
    

def send_to_redakcia(bulletin):
    import requests
    token = os.getenv("LUXTV_BOT_TOKEN")
    chat_id = os.getenv("LUXTV_CHAT_ID")
    parts = [bulletin[i:i+4000] for i in range(0, len(bulletin), 4000)]
    for part in parts:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": part, "link_preview_options": {"is_disabled": True}}
        )
        print(r.json())
    print("✅ Выпуск отправлен в редакцию!")

def get_seen_titles():
    import json
    from datetime import date
    fname = f"seen_titles_{date.today()}.json"
    try:
        with open(fname, 'r') as f:
            return set(json.load(f))
    except:
        return set()

def save_seen_titles(titles):
    import json
    from datetime import date
    fname = f"seen_titles_{date.today()}.json"
    with open(fname, 'w') as f:
        json.dump(list(titles), f)

def run_tv_agent():
    from collector_tv import collect_tv_news, format_tv_for_agent
    seen = get_seen_titles()
    all_news = collect_tv_news()
    news = [n for n in all_news if n['title'] not in seen]
    new_titles = {n['title'] for n in news}
    save_seen_titles(seen | new_titles)
    news_text = format_tv_for_agent(news)
    bulletin = generate_tv_bulletin(news_text)

    attempt = 1
    while bulletin.count("(RU)") < 10 and attempt < 3:
        bulletin = generate_tv_bulletin(news_text)
        attempt += 1

    path = save_bulletin(bulletin)
    send_to_redakcia(bulletin)

if __name__ == "__main__":
    run_tv_agent()
