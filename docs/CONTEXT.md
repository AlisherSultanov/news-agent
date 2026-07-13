# AI News Agent — LUX TV «Yangi Xabarlar 5 Daqiqada»

## КТО АЛИШЕР И КАК С НИМ РАБОТАТЬ

**Алишер Султанов** — основатель LUX TV (ООО «Business Market Media»), Ташкент, Узбекистан.
- Рабочий язык: **русский**
- НЕ программист — работаем пошагово, один шаг за раз
- Давай **одну готовую команду** — копируй и вставляй в терминал
- Никогда не давай несколько вариантов — говори конкретно что делать
- Не повторяй одно и то же несколько раз

---

## ПРОЕКТ: AI News Agent

### Стек
- Mac, Python 3.14, VS Code
- Папка проекта: `~/Documents/news-agent`
- Виртуальное окружение: `.venv`
- Активация: `cd ~/Documents/news-agent && source .venv/bin/activate`

### Файлы проекта

| Файл | Назначение |
|---|---|
| `collector_tv.py` | Коллектор новостей для телепередачи |
| `main_tv.py` | Главный агент — генерирует выпуск и отправляет в Telegram |
| `scheduler.py` | Планировщик — запускает агент 5 раз в день |
| `Procfile` | Команда запуска для Railway: `worker: python scheduler.py` |
| `requirements.txt` | Список библиотек для Railway |
| `.env` | API ключи (не загружается на GitHub) |
| `collector.py` | Старый коллектор для @panorama_uzb (не трогать) |
| `main.py` | Старый агент для @panorama_uzb (не трогать) |

### .env содержит
```
ANTHROPIC_API_KEY=sk-ant-api03-caqQQUW5oUV6tZok9aGwcnWvhxqmgxM4lbEFMkFNkaCHUhz2UNeEp4Xpp_KQ5rzN-VHeI4GmPTRbWmxm_F5kRQ-bbZrRAAA
TELEGRAM_BOT_TOKEN=8695515578:AAFwk...
LUXTV_BOT_TOKEN=8925086230:AAG7y...
LUXTV_CHAT_ID=-5167537573
```

---

## ТЕКУЩЕЕ СОСТОЯНИЕ (обновлено 24.06.2026)

### ✅ Что сделано и работает
1. **collector_tv.py** — 12 рабочих источников, собирает 39 новостей
2. **main_tv.py** — генерирует двуязычный выпуск (узбекский латиница + русский) и **автоматически отправляет в Telegram** группу редакции
3. **scheduler.py** — настроен на 09:00, 12:00, 15:00, 18:00, 21:00 по Ташкенту
4. **Procfile** — добавлен, Railway автоматически запускает `python scheduler.py` при старте
5. **GitHub** — код на `https://github.com/AlisherSultanov/news-agent`
6. **Railway** — задеплоен, статус **Онлайн**, планировщик запущен (`python scheduler.py` подтверждён через консоль)
7. **ANTHROPIC_API_KEY** — обновлён в переменных Railway (старый не работал)
8. **requirements.txt** — включает beautifulsoup4, feedparser, requests, python-dotenv, apscheduler

### ⚠️ Важно про Railway
- Осталось **29 дней или $4.98** — нужно перейти на Hobby план $5/месяц
- Проект называется **«газетный киоск»** (в интерфейсе — «пленительная тишина»)
- Если агент перестал работать — проверить баланс Railway

### Рабочие источники в collector_tv.py (12 штук, 39 новостей)
```python
# Узбекские СМИ
{'name': 'Gazeta.uz', 'url': 'https://www.gazeta.uz/ru/rss/'},
{'name': 'Podrobno.uz', 'url': 'https://podrobno.uz/rss/'},
{'name': 'Uzdaily.uz', 'url': 'https://www.uzdaily.uz/en/rss'},
{'name': 'Sports.uz', 'url': 'https://sports.uz/ru/rss/'},
{'name': 'NUZ.uz', 'url': 'https://nuz.uz/feed'},
{'name': 'Kun.uz', 'url': 'https://kun.uz/news/rss'},
# Мировой шоу-биз
{'name': 'Variety', 'url': 'https://variety.com/feed/'},
{'name': 'Billboard', 'url': 'https://www.billboard.com/feed/'},
{'name': 'Hollywood Reporter', 'url': 'https://www.hollywoodreporter.com/feed/'},
{'name': 'TMZ', 'url': 'https://www.tmz.com/rss.xml'},
{'name': 'Deadline', 'url': 'https://deadline.com/feed/'},
{'name': 'Bollywood Hungama', 'url': 'https://www.bollywoodhungama.com/rss/news.xml'},
{'name': 'Turkish Drama', 'url': 'https://www.turkishdrama.com/feed/'},
```

**Не работают:** Daryo.uz, Repost.uz, Teammy, People, Google News RSS, Hurriyet, Milliyet

**Важно:** использовать `requests.get(url, headers=HEADERS)` а НЕ `feedparser.parse(url)` напрямую:
```python
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
```

---

## КАК РАБОТАЕТ АВТООТПРАВКА

`main_tv.py` при запуске вызывает `run_tv_agent()` которая:
1. Собирает новости через `collector_tv.py`
2. Генерирует выпуск через Claude API
3. Сохраняет в файл `tv_bulletin_YYYYMMDD_HHMM.txt`
4. **Автоматически отправляет в Telegram** через `send_to_redakcia(bulletin)`

Запуск: `python3 main_tv.py`

---

## TELEGRAM

**Группа редакции:**
- Название: LUX TV — Yangi Xabarlar
- Бот: `@luxtv_redakcia_bot`
- ID: `-5167537573`
- Переменная: `LUXTV_BOT_TOKEN`

---

## ДЕПЛОЙ НА RAILWAY

**Как обновить код:**
```bash
cd ~/Documents/news-agent && git add -A && git commit -m "update" && git push
```
Railway автоматически подхватывает изменения из GitHub.

**Если Railway упал:**
1. railway.com → Dashboard → captivating-quietude → газетный киоск → Развертывания → Просмотреть журналы
2. Проверить баланс
3. Проверить переменные окружения

---

## ЧТО ОСТАЛОСЬ СДЕЛАТЬ

1. **Качество фильтрации** — иногда проходит политика и экономика. Нужно улучшить промпт в `main_tv.py`
2. **Узбекские блогеры** — нет источников. Kun.uz частично помогает
3. **Daryo.uz** — RSS не работает
4. **Оплата Railway** — перейти на Hobby план $5/месяц через 29 дней

---

## КОНТАКТЫ
- Телефон: +998998188818
- Email: alishersultanov90@gmail.com
