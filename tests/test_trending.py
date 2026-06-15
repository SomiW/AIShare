from pathlib import Path
import unittest

from scripts.update_trending import (
    Repository,
    deduplicate_repositories,
    is_ai_repository,
    parse_trending,
    render_trending_section,
    replace_trending_section,
    select_repositories,
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

    def test_selects_separate_ai_and_development_lists(self):
        repositories = deduplicate_repositories(
            parse_trending(FIXTURE.read_text(encoding="utf-8"))
        )

        ai_repositories, development_repositories = select_repositories(
            repositories,
            limit=5,
        )

        self.assertEqual(
            [repository.name for repository in ai_repositories],
            ["openai/openai-agents-python"],
        )
        self.assertEqual(
            [repository.name for repository in development_repositories],
            ["astral-sh/ruff"],
        )


class TrendingRenderingTests(unittest.TestCase):
    def setUp(self):
        self.ai_repository = Repository(
            name="openai/openai-agents-python",
            url="https://github.com/openai/openai-agents-python",
            description="Agents & <tools>",
            language="Python",
            stars=12345,
            stars_today=1234,
        )
        self.development_repository = Repository(
            name="astral-sh/ruff",
            url="https://github.com/astral-sh/ruff",
            description="Fast Python tooling.",
            language="Rust",
            stars=40001,
            stars_today=321,
        )

    def test_renders_two_ranked_lists_and_metadata(self):
        section = render_trending_section(
            [self.ai_repository],
            [self.development_repository],
            generated_date="2026-06-15",
        )

        self.assertIn('id="trending"', section)
        self.assertIn("AI 热门", section)
        self.assertIn("开发热门", section)
        self.assertIn("2026-06-15", section)
        self.assertIn("1,234 stars today", section)
        self.assertIn("321 stars today", section)
        self.assertIn("Agents &amp; &lt;tools&gt;", section)
        self.assertIn("https://github.com/trending", section)

    def test_replaces_only_the_marker_delimited_section(self):
        document = (
            "<main>\n"
            "<!-- GITHUB_TRENDING_START -->\n"
            "<section>Old</section>\n"
            "<!-- GITHUB_TRENDING_END -->\n"
            "<section>Keep</section>\n"
            "</main>\n"
        )

        updated = replace_trending_section(document, "<section>New</section>")

        self.assertIn("<section>New</section>", updated)
        self.assertNotIn("<section>Old</section>", updated)
        self.assertIn("<section>Keep</section>", updated)
        self.assertEqual(updated.count("GITHUB_TRENDING_START"), 1)
        self.assertEqual(updated.count("GITHUB_TRENDING_END"), 1)


if __name__ == "__main__":
    unittest.main()
