from pathlib import Path
import unittest

from scripts.update_trending import (
    deduplicate_repositories,
    is_ai_repository,
    parse_trending,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "github-trending.html"


class TrendingParserTests(unittest.TestCase):
    def test_parses_repository_cards(self):
        repositories = parse_trending(FIXTURE.read_text(encoding="utf-8"))

        self.assertEqual(len(repositories), 3)
        self.assertEqual(repositories[0].name, "openai/openai-agents-python")
        self.assertEqual(
            repositories[0].url,
            "https://github.com/openai/openai-agents-python",
        )
        self.assertEqual(
            repositories[0].description,
            "A lightweight framework for building multi-agent workflows.",
        )
        self.assertEqual(repositories[0].language, "Python")
        self.assertEqual(repositories[0].stars, 12345)
        self.assertEqual(repositories[0].stars_today, 1234)

    def test_deduplicates_repositories_by_name(self):
        repositories = parse_trending(FIXTURE.read_text(encoding="utf-8"))

        unique = deduplicate_repositories(repositories)

        self.assertEqual(
            [repository.name for repository in unique],
            ["openai/openai-agents-python", "astral-sh/ruff"],
        )

    def test_classifies_ai_repositories(self):
        repositories = parse_trending(FIXTURE.read_text(encoding="utf-8"))

        self.assertTrue(is_ai_repository(repositories[0]))
        self.assertFalse(is_ai_repository(repositories[1]))


if __name__ == "__main__":
    unittest.main()
