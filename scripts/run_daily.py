"""每日总调度：拉取 → 校验 → 生成 → 缓存。"""
import json
import sys
from config import CACHE_FILE, MIN_GENERAL, MIN_TECH
from fetch_news import fetch_all
from generate_site import write_site


def _load_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("general", []), data.get("tech", [])
    except Exception:
        return [], []


def _save_cache(general, tech):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"general": general, "tech": tech}, f, ensure_ascii=False, indent=2)


def main():
    print("=== 每日新闻抓取 ===")
    general, tech = fetch_all()
    print(f"  总计: {len(general)} 要闻 / {len(tech)} 科技")

    cache_g, cache_t = _load_cache()

    if len(general) < MIN_GENERAL:
        print(f"  要闻不足 {MIN_GENERAL} 条，使用缓存补充")
        general = general + [a for a in cache_g if a not in general]
        general = general[:10]

    if len(tech) < MIN_TECH:
        print(f"  科技不足 {MIN_TECH} 条，使用缓存补充")
        tech = tech + [a for a in cache_t if a not in tech]
        tech = tech[:5]

    if not general and not tech:
        print("  ERROR: 无任何新闻，退出。")
        sys.exit(1)

    write_site(general, tech)
    _save_cache(general, tech)
    print("=== 完成 ===")


if __name__ == "__main__":
    main()
