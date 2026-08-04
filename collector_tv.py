import requests
import feedparser
from datetime import datetime

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

TV_SOURCES = [
    {'name': 'Variety', 'url': 'https://variety.com/feed/'},
    {'name': 'Billboard', 'url': 'https://www.billboard.com/feed/'},
    {'name': 'Hollywood Reporter', 'url': 'https://www.hollywoodreporter.com/feed/'},
    {'name': 'TMZ', 'url': 'https://www.tmz.com/rss.xml'},
    {'name': 'Deadline', 'url': 'https://deadline.com/feed/'},
    {'name': 'Bollywood Hungama', 'url': 'https://www.bollywoodhungama.com/rss/news.xml'},
    {'name': 'Koimoi', 'url': 'https://www.koimoi.com/feed/'},
    {'name': 'Soompi', 'url': 'https://www.soompi.com/feed/'},
    {'name': 'Turkish Drama World', 'url': 'https://turkishdramaworld.com/feed/'},
]


def collect_daryo_showbiz(max_items=4):
    import json as _json
    import re as _re
    from datetime import datetime as _dt

    results = []
    try:
        page_url = "https://daryo.uz/category/madaniyat/"
        r = requests.get(page_url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        m = _re.search(
            r'<script[^>]+id="__NUXT_DATA__"[^>]*>(.*?)</script>',
            r.text,
            _re.S,
        )
        if not m:
            print("Daryo: NUXT_DATA blok topilmadi")
            return results

        flat = _json.loads(m.group(1))
        count = 0
        for val in flat:
            if count >= max_items:
                break
            if isinstance(val, dict) and val.get("category_slug") is not None and "title" in val:
                def resolve(key):
                    idx = val.get(key)
                    return flat[idx] if isinstance(idx, int) else idx

                cat_slug = resolve("category_slug")
                if cat_slug != "show-business":
                    continue

                title = (resolve("title") or "").strip()
                slug = resolve("slug") or ""
                short_content = resolve("short_content") or ""
                date_str = resolve("date") or str(_dt.now())

                summary = _re.sub(r"<[^>]+>", "", short_content).strip()

                try:
                    date_part = date_str.split(" ")[0]
                    y, mo, d = date_part.split("-")
                    link = f"https://daryo.uz/{y}/{mo}/{d}/{slug}"
                except Exception:
                    link = f"https://daryo.uz/{slug}"

                if not title:
                    continue

                results.append({
                    "source": "Daryo",
                    "title": title,
                    "summary": summary[:300],
                    "link": link,
                    "published": date_str,
                })
                count += 1
    except Exception as e:
        print("Daryo: xato -", str(e))
    return results

def collect_tv_news(max_per_source=3, hours=24):
    all_news = []
    seen_titles = set()

    for source in TV_SOURCES:
        sname = source['name']
        count = 0
        try:
            r = requests.get(source['url'], headers=HEADERS, timeout=10)
            feed = feedparser.parse(r.text)
            for entry in feed.entries:
                if count >= max_per_source:
                    break
                title = entry.get('title', '').strip()
                link = entry.get('link', '')
                summary = entry.get('summary', '')
                published = entry.get('published', str(datetime.now()))
                if title in seen_titles or not title:
                    continue
                seen_titles.add(title)
                all_news.append({
                    'source': sname,
                    'title': title,
                    'summary': summary[:300] if summary else '',
                    'link': link,
                    'published': published
                })
                count += 1
            print(sname + ': ' + str(count))
        except Exception as e:
            print(sname + ': xato - ' + str(e))

    try:
        daryo_news = collect_daryo_showbiz()
        all_news.extend(daryo_news)
        print('Daryo:', len(daryo_news))
    except Exception as e:
        print('Daryo umumiy xato -', str(e))

    return all_news

def format_tv_for_agent(news_list):
    result = 'Yangiliklar\n' + '='*50 + '\n\n'
    for i, n in enumerate(news_list, 1):
        result += f"{i}. [{n['source']}]\n"
        result += 'Sarlavha: ' + n['title'] + '\n'
        if n['summary']:
            result += 'Tavsif: ' + n['summary'] + '\n'
        result += 'Sana: ' + n['published'] + '\n'
        result += 'Manba: ' + n['source'] + '\n'
        result += 'Havola: ' + n['link'] + '\n'
        result += '-'*30 + '\n'
    return result

if __name__ == '__main__':
    news = collect_tv_news()
    print('\nJami: ' + str(len(news)) + ' yangilik')
