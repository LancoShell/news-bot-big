import logging
import requests

logger = logging.getLogger(__name__)


def _fetch(url: str, params: dict) -> list[dict]:
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    logger.info("NewsAPI response: %s", data)
    if data.get("status") == "error":
        raise RuntimeError(f"NewsAPI error {data.get('code')}: {data.get('message')}")
    response.raise_for_status()
    return data.get("articles", [])


def get_top_news(api_key: str) -> list[dict]:
    articles = _fetch("https://newsapi.org/v2/everything", {
        "q": "italia",
        "language": "it",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": api_key,
    })
    return articles[:5]


def get_tech_news(api_key: str) -> list[dict]:
    articles = _fetch("https://newsapi.org/v2/everything", {
        "q": "tecnologia OR intelligenza artificiale OR cybersecurity OR informatica",
        "language": "it",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": api_key,
    })
    return articles[:5]


def format_articles(articles: list[dict], header: str) -> str:
    if not articles:
        return "Nessuna notizia trovata al momento."

    lines = [f"<b>{header}</b>", ""]
    for i, article in enumerate(articles, start=1):
        title = article.get("title") or "Titolo non disponibile"
        description = article.get("description") or ""
        url = article.get("url") or ""

        if len(description) > 150:
            description = description[:147] + "..."

        lines.append(f"{i}. <b>{escape_html(title)}</b>")
        if description:
            lines.append(f"   {escape_html(description)}")
        if url:
            lines.append(f'   🔗 <a href="{url}">Leggi l\'articolo</a>')
        lines.append("")

    return "\n".join(lines).strip()


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
