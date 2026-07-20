import anthropic
import os
from dotenv import load_dotenv
from collector_tv import collect_tv_news, format_tv_for_agent

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PROMPT = """Ты — редактор узбекского телевизионного шоу-биз выпуска «Yulduzlar Dunyosi» на LUX TV.
Твоя задача — на основе предоставленных новостей собрать готовый выпуск: закадровый текст, источники, фото/видео рекомендации.

ПАРАМЕТРЫ ВЫПУСКА:
- Слов на новость: 100–120 слов (50–60 секунд)
- Всего новостей: 5
- Свежесть: только за последние 24 часа

ТЕМАТИКА — брать ТОЛЬКО:
- Индийское кино и Болливуд — премьеры, трейлеры, звёзды (ВЫСШИЙ ПРИОРИТЕТ)
- Узбекский шоу-бизнес — певцы, актёры, блогеры, знаменитости
- Мировой шоу-бизнес — Голливуд, K-pop, турецкие сериалы, звёзды
- Кино и сериалы — Netflix, HBO, новые релизы, награды
- Жизнь звёзд — скандалы, свадьбы, премьеры, интервью
- Музыкальные новости — хиты, альбомы, концерты мировых звёзд

ЗАПРЕЩЁННЫЕ ТЕМЫ — не брать никогда:
- Политика — выборы, правительство, законы, дипломатия
- Спорт — кроме случаев когда спортсмен замешан в скандале или свадьбе
- Экономика, финансы, бизнес-новости
- Религия
- Контент 18+
- Криминал БЕЗ связи с известной личностью
- Региональные новости без шоу-биз контекста

ОТБОР НОВОСТЕЙ:
- Выбирай самое резонансное и интересное зрителю
- Нет жёсткого приоритета по географии — узбекское или мировое, главное ИНТЕРЕСНО
- Если есть горячая мировая новость — она важнее слабой узбекской
- Индийское кино всегда в приоритете при прочих равных

АТРИБУЦИЯ — каждая новость начинается с одной фразы:
Reuters ma'lumotiga ko'ra... / Rasmiiy manbalar xabar berishicha... / AP agentligi xabar beradi...

СТРУКТУРА ВЫПУСКА:
————————————————————————————
[ЗАСТАВКА — 5 секунд]

ОТКРЫТИЕ: «Yulduzlar Dunyosi. Boshlaylik.»

НОВОСТЬ 1
НОВОСТЬ 2
НОВОСТЬ 3
НОВОСТЬ 4
НОВОСТЬ 5

ЗАКРЫТИЕ: «Yulduzlar Dunyosi. Ko'rishguncha.»
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

## ТЕХНИЧЕСКИЕ ПАРАМЕТРЫ
| Параметр | Значение |
|---|---|
| Общий хронометраж | ~600 слов |
| Новостей | 5 |
| Хронометраж | 5 минут |

## ИЗОХ МУҲАРРИР УЧУН:
⚠️ Если среди новостей нет подходящего шоу-биз контента — напиши об этом явно и объясни почему каждая новость не подходит. Не составляй выпуск из неподходящих новостей."""

def generate_tv_bulletin(news_text):
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": f"{PROMPT}\n\nВот новости для выпуска:\n\n{news_text}"
            }
        ]
    )
    return message.content[0].text

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

def run_tv_agent():
    from collector_tv import collect_tv_news, format_tv_for_agent
    news = collect_tv_news()
    news_text = format_tv_for_agent(news)
    bulletin = generate_tv_bulletin(news_text)
    path = save_bulletin(bulletin)
    send_to_redakcia(bulletin)

if __name__ == "__main__":
    run_tv_agent()
