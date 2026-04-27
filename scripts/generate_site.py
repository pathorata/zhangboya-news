"""从新闻数据生成 index.html。"""
import html
import re
from datetime import datetime
from config import OUTPUT_HTML


def _esc(text):
    """去掉 HTML 标签并转义，截断到 200 字。"""
    clean = re.sub(r"<[^>]+>", "", text or "")
    return html.escape(clean[:200])


def build_html(general_news, tech_news):
    """返回完整的 index.html 字符串。"""
    now_str = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    def card(article, idx, accent_class="", tag_class=""):
        return f"""
        <article class="news-card{accent_class}">
            <span class="rank">#{idx}</span>
            <div class="card-body">
                <h3><a href="{_esc(article['link'])}" target="_blank" rel="noopener">
                    {_esc(article['title'])}
                </a></h3>
                <p class="summary">{_esc(article['summary'])}</p>
                <span class="source-tag{tag_class}">{_esc(article['source'])}</span>
            </div>
        </article>"""

    general_cards = "\n".join(card(a, i + 1) for i, a in enumerate(general_news))
    tech_cards = "\n".join(
        card(a, i + 1, " tech-card", " tech-tag") for i, a in enumerate(tech_news)
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日要闻 — zhangboya.top</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>每日要闻</h1>
        <p class="subtitle">每日十大要闻 + 五大科技动态</p>
        <p class="update-time">更新于 {now_str}（北京时间）</p>
    </header>

    <main>
        <section class="news-section">
            <h2>今日十大要闻</h2>
            <div class="news-grid">{general_cards}
            </div>
        </section>

        <section class="news-section tech-section">
            <h2>科技动态 TOP 5</h2>
            <div class="news-grid">{tech_cards}
            </div>
        </section>
    </main>

    <footer>
        <p>内容来源于各 RSS 源，版权归原作者所有 · Powered by GitHub Pages</p>
    </footer>
</body>
</html>"""


def write_site(general_news, tech_news):
    html_str = build_html(general_news, tech_news)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_str)
    print(f"  已写入 {OUTPUT_HTML}（{len(html_str)} 字节）")
