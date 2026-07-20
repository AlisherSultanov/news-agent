import requests
import feedparser
from datetime import datetime

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

TV_SOURCES = [
    {'name': 'Gazeta.uz', 'url': 'https://www.gazeta.uz/ru/rss/'},
    {'name': 'Podrobno.uz', 'url': 'https://podrobno.uz/rss/'},
    {'name': 'Uzdaily.uz', 'url': 'https://www.uzdaily.uz/en/rss'},
    {'name': 'NUZ.uz', 'url': 'https://nuz.uz/feed'},
    {'name': 'Kun.uz', 'url': 'https://kun.uz/news/rss'},
    {'name': 'Daryo.uz', 'url': 'https://daryo.uz/feed'},
    {'name': 'Uzbekistan Today', 'url': 'https://ut.uz/ru/rss/'},
    {'name': 'Variety', 'url': 'https://variety.com/feed/'},
    {'name': 'Billboard', 'url': 'https://www.billboard.com/feed/'},
    {'name': 'Hollywood Reporter', 'url': 'https://www.hollywoodreporter.com/feed/'},
    {'name': 'TMZ', 'url': 'https://www.tmz.com/rss.xml'},
    {'name': 'Deadline', 'url': 'https://deadline.com/feed/'},
    {'name': 'People', 'url': 'https://people.com/feed/'},
    {'name': 'Bollywood Hungama', 'url': 'https://www.bollywoodhungama.com/rss/news.xml'},
    {'name': 'Pinkvilla', 'url': 'https://www.pinkvilla.com/rss'},
    {'name': 'Koimoi', 'url': 'https://www.koimoi.com/feed/'},
    {'name': 'Soompi', 'url': 'https://www.soompi.com/feed/'},
    {'name': 'Turkish Drama', 'url': 'https://www.turkishdrama.com/feed/'},
]

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
