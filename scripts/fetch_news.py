"""获取 RSS 源，解析文章，去重排序。"""
import feedparser
import requests
from config import (
    GENERAL_SOURCES, TECH_SOURCES, REQUEST_TIMEOUT, USER_AGENT,
)


def fetch_feed(name, url):
    """获取单个 RSS 源，返回文章列表。失败返回 []，不抛异常。"""
    try:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)
        articles = []
        for entry in feed.entries:
            articles.append({
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", ""),
                "summary": _clean_summary(
                    entry.get("summary", entry.get("description", ""))
                ),
                "source": name,
                "published": entry.get("published", entry.get("updated", "")),
            })
        return articles
    except Exception as e:
        print(f"  [{name}] 获取失败: {e}")
        return []


def _clean_summary(raw):
    """去掉 HTML 标签，截断到 200 字。"""
    import re
    text = re.sub(r"<[^>]+>", "", raw or "")
    text = text.replace("\n", " ").replace("\r", " ")
    return text.strip()[:200]


def deduplicate(articles):
    """按标题前 30 字模糊去重。"""
    seen = set()
    unique = []
    for a in articles:
        key = a["title"][:30].replace(" ", "").lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(a)
    return unique


def fetch_all():
    """主入口：获取全部新闻源，去重排序，返回 (要闻列表, 科技列表)。"""
    all_articles = []

    for name, url, is_primary in GENERAL_SOURCES:
        articles = fetch_feed(name, url)
        for a in articles:
            a["category"] = "general"
            a["score"] = 2 if is_primary else 1
        all_articles.extend(articles)
        print(f"  [{name}] {len(articles)} 篇")

    for name, url, is_primary in TECH_SOURCES:
        articles = fetch_feed(name, url)
        for a in articles:
            a["category"] = "tech"
            a["score"] = 2 if is_primary else 1
        all_articles.extend(articles)
        print(f"  [{name}] {len(articles)} 篇")

    unique = deduplicate(all_articles)
    # 按分数降序，同分按发布时间降序
    unique.sort(key=lambda x: (-x["score"], x.get("published", "")), reverse=False)

    general = [a for a in unique if a["category"] == "general"]
    tech = [a for a in unique if a["category"] == "tech"]

    from config import MAX_GENERAL, MAX_TECH
    return general[:MAX_GENERAL], tech[:MAX_TECH]
