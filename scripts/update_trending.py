#!/usr/bin/env python3
"""Fetch and render GitHub Trending repositories."""

from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
import re


GITHUB_ORIGIN = "https://github.com"
AI_KEYWORDS = {
    "agent",
    "agents",
    "ai",
    "artificial intelligence",
    "chatbot",
    "embedding",
    "generative",
    "language model",
    "llm",
    "machine learning",
    "rag",
    "transformer",
}


@dataclass(frozen=True)
class Repository:
    name: str
    url: str
    description: str
    language: str
    stars: int
    stars_today: int


def _clean_text(parts):
    return " ".join(" ".join(parts).split())


def _parse_number(value):
    match = re.search(r"[\d,]+", value)
    return int(match.group(0).replace(",", "")) if match else 0


class TrendingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.repositories = []
        self.card = None
        self.capture = None
        self.capture_parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())

        if tag == "article" and "Box-row" in classes:
            self.card = {
                "name": "",
                "url": "",
                "description": "",
                "language": "",
                "stars": 0,
                "stars_today": 0,
            }
            return

        if self.card is None:
            return

        if tag == "a":
            href = attributes.get("href", "")
            if (
                not self.card["name"]
                and href.count("/") == 2
                and not href.endswith("/stargazers")
            ):
                self.capture = "repository"
                self.capture_parts = []
                self.card["url"] = f"{GITHUB_ORIGIN}{href}"
            elif href.endswith("/stargazers"):
                self.capture = "stars"
                self.capture_parts = []
        elif tag == "p" and "color-fg-muted" in classes:
            self.capture = "description"
            self.capture_parts = []
        elif tag == "span" and attributes.get("itemprop") == "programmingLanguage":
            self.capture = "language"
            self.capture_parts = []
        elif tag == "span" and "float-sm-right" in classes:
            self.capture = "stars_today"
            self.capture_parts = []

    def handle_data(self, data):
        if self.card is not None and self.capture:
            self.capture_parts.append(data)

    def handle_endtag(self, tag):
        if self.card is None:
            return

        expected_tags = {
            "repository": "a",
            "stars": "a",
            "description": "p",
            "language": "span",
            "stars_today": "span",
        }
        if self.capture and expected_tags[self.capture] == tag:
            text = _clean_text(self.capture_parts)
            if self.capture == "repository":
                self.card["name"] = text.replace(" / ", "/").replace(" ", "")
            elif self.capture in {"stars", "stars_today"}:
                self.card[self.capture] = _parse_number(text)
            else:
                self.card[self.capture] = text
            self.capture = None
            self.capture_parts = []

        if tag == "article":
            if self.card["name"]:
                self.repositories.append(Repository(**self.card))
            self.card = None


def parse_trending(source):
    parser = TrendingParser()
    parser.feed(source)
    return parser.repositories


def deduplicate_repositories(repositories):
    unique = {}
    for repository in repositories:
        unique.setdefault(repository.name.lower(), repository)
    return list(unique.values())


def is_ai_repository(repository):
    searchable = f"{repository.name} {repository.description}".lower()
    return any(keyword in searchable for keyword in AI_KEYWORDS)


def _render_repository(repository, rank):
    language = escape(repository.language or "未标注")
    return f"""          <li class="trending-item">
            <span class="trending-rank">{rank:02d}</span>
            <div class="trending-copy">
              <h3><a href="{escape(repository.url, quote=True)}">{escape(repository.name)}</a></h3>
              <p>{escape(repository.description or "暂无项目简介。")}</p>
              <div class="trending-meta">
                <span>{language}</span>
                <span>{repository.stars_today:,} stars today</span>
                <span>{repository.stars:,} total</span>
              </div>
            </div>
          </li>"""


def _render_list(title, subtitle, repositories, accent):
    items = "\n".join(
        _render_repository(repository, rank)
        for rank, repository in enumerate(repositories, start=1)
    )
    return f"""      <section class="trending-panel {accent}">
        <div class="trending-panel-heading">
          <div>
            <p class="section-kicker">Daily ranking</p>
            <h3>{escape(title)}</h3>
          </div>
          <span>{escape(subtitle)}</span>
        </div>
        <ol class="trending-list">
{items}
        </ol>
      </section>"""


def render_trending_section(ai_repositories, development_repositories, generated_date):
    ai_panel = _render_list(
        "AI 热门",
        "模型、Agent 与智能应用",
        ai_repositories,
        "trending-ai",
    )
    development_panel = _render_list(
        "开发热门",
        "工程工具与开源基础设施",
        development_repositories,
        "trending-dev",
    )
    return f"""    <section class="trending section-shell" id="trending">
      <div class="section-heading trending-heading">
        <div>
          <p class="section-kicker">Trending today</p>
          <h2>今日热门 <span>每日更新</span></h2>
        </div>
        <p>
          更新于 {escape(generated_date)} · 数据来源
          <a href="https://github.com/trending">GitHub Trending ↗</a>
        </p>
      </div>
      <div class="trending-grid">
{ai_panel}
{development_panel}
      </div>
    </section>"""


def replace_trending_section(document, section):
    start_marker = "<!-- GITHUB_TRENDING_START -->"
    end_marker = "<!-- GITHUB_TRENDING_END -->"
    if document.count(start_marker) != 1 or document.count(end_marker) != 1:
        raise ValueError("Expected exactly one GitHub Trending marker pair")
    before, remainder = document.split(start_marker, maxsplit=1)
    _, after = remainder.split(end_marker, maxsplit=1)
    return (
        f"{before}{start_marker}\n"
        f"{section}\n"
        f"    {end_marker}{after}"
    )
