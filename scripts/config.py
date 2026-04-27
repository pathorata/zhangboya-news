"""一切可配置项集中在这里。修改新闻源只需改这个文件。"""

# ── 要闻源 ──
GENERAL_SOURCES = [
    ("人民网-要闻", "http://www.people.com.cn/rss/yw.xml", True),
    ("新华网-头条", "http://www.xinhuanet.com/rss/title.xml", True),
    ("联合早报-中港台", "https://www.zaobao.com/rss/china", True),
    ("参考消息-滚动", "http://www.cankaoxiaoxi.com/rss/roll.xml", True),
    ("环球网", "https://www.huanqiu.com/rss/news.xml", False),
]

# ── 科技源 ──
TECH_SOURCES = [
    ("36氪", "https://36kr.com/feed", True),
    ("少数派", "https://sspai.com/feed", True),
    ("开源中国", "https://www.oschina.net/news/rss", True),
    ("虎嗅", "https://www.huxiu.com/rss/0.xml", True),
    ("InfoQ中国", "https://www.infoq.cn/feed", False),
]

MAX_GENERAL = 10    # 每日要闻条数
MAX_TECH = 5        # 每日科技条数
MIN_GENERAL = 3     # 少于这个数就用缓存兜底
MIN_TECH = 2

REQUEST_TIMEOUT = 15  # 秒
USER_AGENT = (
    "Mozilla/5.0 (compatible; NewsAggregator/1.0; +https://zhangboya.top)"
)

OUTPUT_HTML = "docs/index.html"
CACHE_FILE = "docs/news_cache.json"
