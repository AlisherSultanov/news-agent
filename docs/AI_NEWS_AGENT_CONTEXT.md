# SKILL: AI News Agent — LUX TV «Yangi Xabarlar 5 Daqiqada»

## КТО АЛИШЕР И КАК С НИМ РАБОТАТЬ

**Алишер Султанов** — основатель LUX TV (ООО «Business Market Media»), Ташкент, Узбекистан.
- Рабочий язык: **русский**
- НЕ программист — работаем пошагово, один шаг за раз
- После каждого шага ждёт скриншот от него
- Давай **одну готовую команду** — копируй и вставляй в терминал
- Никогда не давай несколько вариантов — говори конкретно что делать
- Объясняй детально и просто — куда нажать, что написать
- Не повторяй одно и то же несколько раз
- Если нужно посмотреть файл — давай одну команду которая покажет всё целиком

---

## ПРОЕКТ: AI News Agent

### Что это
Автоматический агент который собирает новости, генерирует 5-минутный телевизионный выпуск и отправляет в Telegram группу редакции LUX TV. Работает 5 раз в день без участия человека.

### Стек
- Mac, Python 3.14, VS Code
- Папка проекта: `~/Documents/news-agent`
- Виртуальное окружение: `.venv`
- Активация: `cd ~/Documents/news-agent && source .venv/bin/activate`

### Файлы проекта

| Файл | Назначение |
|---|---|
| `collector_tv.py` | Коллектор новостей для телепередачи |
| `main_tv.py` | Главный агент — генерирует выпуск через Claude API |
| `scheduler.py` | Планировщик — запускает агент 5 раз в день |
| `requirements.txt` | Список библиотек для Railway |
| `.env` | API ключи (не загружается на GitHub) |
| `collector.py` | Старый коллектор для @panorama_uzb (не трогать) |
| `main.py` | Старый агент для @panorama_uzb (не трогать) |

### .env содержит
```
ANTHROPIC_API_KEY=sk-ant-api03-...
TELEGRAM_BOT_TOKEN=8695515578:AAFwk...
LUXTV_BOT_TOKEN=8925086230:AAG7y...
LUXTV_CHAT_ID=-5167537573
```

---

## ТЕКУЩЕЕ СОСТОЯНИЕ (обновлено 23.06.2026)

### ✅ Что сделано и работает
1. **collector_tv.py** — 12 рабочих источников, собирает 39 новостей.
2. **main_tv.py** — генерирует двуязычный выпуск (узбекский латиница + русский). Отправляет в группу редакции.
3. **scheduler.py** — настроен на 09:00, 12:00, 15:00, 18:00, 21:00 по Ташкенту (Asia/Tashkent).
4. **GitHub** — код на `https://github.com/AlisherSultanov/news-agent`
5. **Railway** — задеплоен, статус **Онлайн**. Команда запуска: `python scheduler.py`.
6. **requirements.txt** — включает beautifulsoup4, feedparser, requests, python-dotenv, apscheduler и др.

### ⚠️ Важно про Railway
- Railway бесплатно даёт **$5 на 30 дней**
- После этого нужен план **Hobby за $5/месяц**
- Если агент вдруг перестал работать — первым делом проверить Railway не кончились ли деньги
- Проект называется **«газетный киоск»**

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

**Не работают** (давали 0 новостей): Daryo.uz, Repost.uz, Teammy, People, Kun.uz RSS (старый), Google News RSS, Hurriyet, Milliyet, Pinkvilla, Filmfare, Goal.com

**Важно для collector_tv.py**: использовать `requests.get(url, headers=HEADERS)` а НЕ `feedparser.parse(url)` напрямую. Правильный HEADERS:
```python
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
```

---

## ФОРМАТ ВЫПУСКА (main_tv.py)

**Хронометраж:** 5 минут  
**Новостей:** 5 историй  
**Языки:** узбекский (латиница) + русский — оба обязательны  
**Без ведущего** — только закадровый голос

**Тематика (приоритет):**
1. Узбекское кино, шоу-биз, блогеры
2. Индийское кино (Болливуд)
3. Турецкое кино (сериалы)
4. Мировые звёзды (Голливуд, музыка)
5. Спорт — только звёзды (Хусанов, Шомуродов)
6. Бизнес — только известные с резонансом

**Запрещено:** политика, религия, 18+, мелкий криминал

**Формат каждой новости:**
```
НОВОСТЬ [№]
─────────────────────────────────────────
ТЕКСТ (o'zbekcha):
[закадровый текст на узбекском латиницей, 100-120 слов]

ТЕКСТ (русский):
[тот же текст на русском, 100-120 слов]

ИСТОЧНИК: [название СМИ]
ССЫЛКА НА СТАТЬЮ: [https://...]

ВИДЕО/ФОТО:
— Что показывать: [описание на узбекском латиницей]
— Где скачать: [Instagram @username / Getty Images / YouTube + ссылка]
— РИСК: [без риска / низкий / средний / высокий]

ГРАФИКА: [максимум 3 слова]
─────────────────────────────────────────
```

---

## TELEGRAM

**Группа редакции:**
- Название: LUX TV — Yangi Xabarlar
- Бот: `@luxtv_redakcia_bot`
- ID: `-5167537573`
- Переменная: `LUXTV_BOT_TOKEN`

**Отправка выпуска вручную:**
```bash
cd ~/Documents/news-agent && source .venv/bin/activate && python3 -c "from main_tv import send_to_redakcia; send_to_redakcia(open('tv_bulletin_YYYYMMDD_HHMM.txt').read())"
```
(заменить имя файла на актуальное)

**Запуск полного теста вручную:**
```bash
cd ~/Documents/news-agent && source .venv/bin/activate && python3 main_tv.py
```

---

## ДЕПЛОЙ НА RAILWAY

**Аккаунт:** GitHub `AlisherSultanov`, связан с Railway  
**Проект:** «газетный киоск» на railway.com  
**Команда запуска:** `python scheduler.py`

**Как обновить код на Railway:**
```bash
cd ~/Documents/news-agent && git add -A && git commit -m "update" && git push
```
Railway автоматически подхватывает изменения из GitHub.

**Если Railway упал — проверить:**
1. railway.app → проект → вкладка «Развертывания» → «Просмотреть журналы»
2. Проверить баланс (не кончились ли $5)
3. Проверить переменные окружения во вкладке «Переменные»

---

## ЧТО ОСТАЛОСЬ СДЕЛАТЬ

1. **Качество фильтрации** — агент иногда берёт политику и экономику вместо шоу-биза. Нужно улучшить промпт в main_tv.py.
2. **Блогеры** — нет источников которые пишут про узбекских блогеров. Kun.uz частично помогает.
3. **Daryo.uz** — RSS не работает через стандартный запрос. Нужен скрейпинг.
4. **Оплата Railway** — через 30 дней нужно перейти на Hobby план $5/месяц.

---

## КОНТАКТЫ АЛИШЕРА
- Телефон: +998998188818
- Email: alishersultanov90@gmail.com
