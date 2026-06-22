import feedparser, requests
from datetime import datetime, timedelta
from dateutil import parser as dateparser

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

TV_SOURCES = [
    # Официальные УЗ
    {'name': 'President.uz', 'url': 'https://president.uz/ru/rss'},
    {'name': 'Minkultura', 'url': 'https://mcu.uz/ru/rss'},
    {'name': 'Sport.uz', 'url': 'https://sport.uz/rss'},
    {'name': 'UFA.uz', 'url': 'https://ufa.uz/rss'},
    {'name': 'Olympic.uz', 'url': 'https://olympic.uz/rss'},
    # Узбекские СМИ
    {'name': 'Kun.uz', 'url': 'https://kun.uz/rss'},
    {'name': 'Gazeta.uz', 'url': 'https://www.gazeta.uz/ru/rss/'},
    {'name': 'Daryo.uz', 'url': 'https://daryo.uz/rss'},
    {'name': 'Podrobno.uz', 'url': 'https://podrobno.uz/rss/'},
    {'name': 'Uzdaily.uz', 'url': 'https://uzdaily.uz/rss'},
    {'name': 'Sports.uz', 'url': 'https://sports.uz/rss'},
    {'name': 'Orienews.uz', 'url': 'https://orienews.uz/rss'},
    # Мировой шоу-биз
    {'name': 'Variety', 'url': 'https://variety.com/feed/'},
    {'name': 'Billboard', 'url': 'https://www.billboard.com/feed/'},
    {'name': 'Hollywood Reporter', 'url': 'https://www.hollywoodreporter.com/feed/'},
    {'name': 'TMZ', 'url': 'https://www.tmz.com/rss.xml'},
    {'name': 'Deadline', 'url': 'https://deadline.com/feed/'},
    # Индийское кино
    {'name': 'Bollywood Hungama', 'url': 'https://www.bollywoodhungama.com/rss/news.xml'},
    {'name': 'Pinkvilla', 'url': 'https://www.pinkvilla.com/rss.xml'},
    # Индийское кино — из Индии
    {'name': 'Bollywood Hungama', 'url': 'https://www.bollywoodhungama.com/rss/news.xml'},
    {'name': 'Pinkvilla', 'url': 'https://www.pinkvilla.com/rss.xml'},
    {'name': 'Filmfare', 'url': 'https://www.filmfare.com/rss/rss.xml'},
    {'name': 'NDTV Entertainment', 'url': 'https://feeds.feedburner.com/ndtvmoviesnews'},
    # Турецкое кино — из Турции
    {'name': 'Hurriyet Entertainment', 'url': 'https://www.hurriyet.com.tr/rss/magazin'},
    {'name': 'Milliyet Magazin', 'url': 'https://www.milliyet.com.tr/rss/rssnews/gundem.xml'},
    # Узбекское кино
    {'name': 'Kinokassa.uz', 'url': 'https://kinokassa.uz/rss'},
    # Спорт звёзды
    {'name': 'Goal.com', 'url': 'https://www.goal.com/feeds/en/news'},
]

def collect_tv_news(max_per_source=3, hours=24):
    all_news = []
    seen_titles = set()
    cutoff = datetime.now() - timedelta(hours=hours)
    for source in TV_SOURCES:
        sname = source['name']
        try:
            r = requests.get(source['url'], headers=HEADERS, timeout=8)
            feed = feedparser.parse(r.text)
            count = 0
            for entry in feed.entries[:max_per_source*2]:
                if count >= max_per_source:
                    break
                title = entry.get('title', '').strip()
                if not title or title in seen_titles:
                    continue
                link = entry.get('link', '')
                summary = entry.get('summary', '')
                published = entry.get('published', '')
                try:
                    pd = dateparser.parse(published, ignoretz=True)
                    if pd and pd < cutoff:
                        continue
                except:
                    pass
                seen_titles.add(title)
                all_news.append({'source': sname, 'title': title, 'link': link, 'summary': summary[:300], 'published': published})
                count += 1
            print(sname + ': ' + str(count))
        except Exception as e:
            print(sname + ': xato')
    return all_news

def format_tv_for_agent(news_list):
    result = 'Yangiliklar\n' + '='*50 + '\n\n'
    for i, n in enumerate(news_list, 1):
        result += str(i) + '. [' + n['source'] + ']\n'
        result += 'Sarlavha: ' + n['title'] + '\n'
        if n['summary']:
            result += 'Tavsif: ' + n['summary'] + '\n'
        result += 'Manba: ' + n['source'] + '\n'
        result += 'Havola: ' + n['link'] + '\n'
        result += '-'*30 + '\n'
    return result

if __name__ == '__main__':
    news = collect_tv_news()
    print('\nJami: ' + str(len(news)) + ' yangilik')
