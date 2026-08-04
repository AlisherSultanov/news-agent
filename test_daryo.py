import json
import re
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_nuxt_data(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    m = re.search(
        r'<script[^>]+id="__NUXT_DATA__"[^>]*>(.*?)</script>',
        r.text,
        re.S,
    )
    if not m:
        print("NUXT_DATA blok topilmadi")
        return None
    return json.loads(m.group(1))

def find_news_items(flat):
    items = []
    for i, val in enumerate(flat):
        if isinstance(val, dict) and "category_slug" in val and "title" in val:
            def resolve(key):
                idx = val.get(key)
                return flat[idx] if isinstance(idx, int) else idx
            items.append({
                "category_slug": resolve("category_slug"),
                "title": resolve("title"),
                "slug": resolve("slug"),
                "content": resolve("content"),
                "short_content": resolve("short_content"),
                "date": resolve("date"),
                "created_at": resolve("created_at"),
            })
    return items

if __name__ == "__main__":
    page_url = "https://daryo.uz/category/madaniyat/"
    flat = get_nuxt_data(page_url)
    if flat:
        items = find_news_items(flat)
        sb = [i for i in items if i["category_slug"] == "show-business"]
        print("Show-business yozuvlari:", len(sb))
        for it in sb:
            print(it["title"])
            print("  slug:", it["slug"])
            print("  date:", it["date"])
            print("  created_at:", it["created_at"])
            print()
