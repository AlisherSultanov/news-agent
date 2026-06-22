import requests
import feedparser
from datetime import datetime, timedelta
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Accept": "application/rss+xml, application/xml, text/xml"
}

SEARCH_QUERIES = [
    "uzbek yulduzlar yangiliklari",
    "o'zbek estradasi yangiliklari",
    "uzbekistan kino yangiliklari",
    "uzbek blogerlar yangiliklari",
    "o'zbek kinosi 2026",
    "yangi kinolar 2026",
    "yangi seriallar 2026",
    "turkiy seriallar 2026",
    "korean drama 2026",
    "kinoteatr premyera 2026",
    "Yulduz Usmonova",
    "Munisa Rizayeva",
    "Shahzoda",
    "Rayhona",
    "Bolalar",
    "Nodir Toshpulatov",
    "Shaxlo Otabekova",
    "Ziyoda",
    "Gavhar Toshmatova",
    "Gaybullo",
    "Dilnoza Yusupova",
    "Sherzod va Barno",
    "Humoyun Bekmurodov",
    "Abbos Murtazoyev",
    "Orzu Nazarov",
    "Firdavs Toshmatov",
    "Hulkar Abdullayeva",
    "Sardor Tashkentov",
    "Abdukodir Xusanov",
    "Abdukodir Khusanov Manchester City",
    "BTS kpop",
    "Blackpink",
    "Taylor Swift",
    "MrBeast",
    "Khaby Lame",
    "Drake music",
    "Beyonce",
    "Dua Lipa",
    "new movies 2026",
    "new series 2026",
    "Netflix new 2026",
    "HBO new series 2026",
    "Disney Plus 2026",
    "Hollywood news 2026",
    "Bollywood news 2026",
    "Grammy 2026",
    "Oscar 2026",
    "TikTok trend uzbekistan",
    "YouTube trend uzbekistan",
]

RSS_SOURCES = [
    {"name": "Kun.uz", "url": "https://kun.uz/rss"},
    {"name": "Daryo.uz", "url": "https://daryo.uz/feed"},
    {"name": "Gazeta.uz", "url": "https://www.gazeta.uz/ru/rss/"},
    {"name": "BBC Entertainment", "url": "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml"},
    {"name": "BBC Sport", "url": "https://feeds.bbci.co.uk/sport/rss.xml"},
    {"name": "Variety", "url": "https://variety.com/feed/"},
    {"name": "Billboard", "url": "https://www.billboard.com/feed/"},
    {"name": "Hollywood Reporter", "url": "https://www.hollywoodreporter.com/feed/"},
    {"name": "Kinopoisk", "url": "https://www.kinopoisk.ru/rss/"},
    {"name": "Goal.com", "url": "https://www.goal.com/feeds/en/news"},
]

def build_sources():
    sources = list(RSS_SOURCES)
    for query in SEARCH_QUERIES:
        q = query.replace(" ", "+").replace("'", "%27")
        sources.append({
            "name": f"Google: {query}",
            "url": f"https://news.google.com/rss/search?q={q}&hl=ru&gl=UZ&ceid=UZ:ru"
        })
    return sources

def collect_news(max_per_source=3):
    all_news = []
    seen_titles = set()
    sources = build_sources()
    cutoff = datetime.now() - timedelta(hours=48)
    print(f"Jami manba3lar: {len(sources)}")
    print("-" * 50)
    for source in sources:
        try:
            response = requests.get(source["url"], headers=HEADERS, timeout=8)
            feed = feedparser.parse(response.text)
            count = 0
            for entry in feed.entries[:max_per_source*3]:
                title = entry.get("title", "")
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    pub = entry.get("published_parsed") or entry.get("updated_parsed")
                    if pub:
                        pub_dt = datetime.fromtimestamp(time.mktime(pub))
                        if pub_dt < cutoff:
                            continue
                    news_item = {
                        "source": source["name"],
                        "title": title,
                        "summary": entry.get("summary", ""),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", "")
                    }
                    all_news.append(news_item)
                    count += 1
                    if count >= max_per_source:
                        break
            if count > 0:
                print(f"+ {source['name']}: {count} yangilik")
        except Exception:
            pass
    return all_news

def format_for_agent(news_list):
    result = f"Yangiliklar yigindi: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    result += "=" * 50 + "\n\n"
    for i, news in enumerate(news_list, 1):
        result += f"{i}. [{news['source']}]\n"
        result += f"Sarlavha: {news['title']}\n"
        if news['summary']:
            result += f"Tavsif: {news['summary'][:200]}\n"
        result += f"Sana: {news['published']}\n\n"
        result += f"Manba: {news['source']}\n"
        result += f"Havola: {news['link']}\n"
    return result

if __name__ == "__main__":
    print("Shoubiznes yangiliklar yiguvchi ishga tushdi!")
    print("=" * 50)
    news = collect_news(max_per_source=3)
    print(f"\nJami yigilgan yangiliklar: {len(news)}")
    if news:
        print("\n" + format_for_agent(news))
    else:
        print("Yangiliklar topilmadi")
