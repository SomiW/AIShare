#!/usr/bin/env python3
"""Fetch and render GitHub Trending repositories."""

from dataclasses import dataclass
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
