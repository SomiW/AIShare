from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
STYLES = ROOT / "styles.css"
WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"
TRENDING_WORKFLOW = ROOT / ".github" / "workflows" / "update-trending.yml"

REQUIRED_SECTIONS = {
    "trending",
    "featured",
    "ai-coding",
    "models",
    "agents",
    "data",
    "editors",
    "quality",
    "devops",
    "contribute",
}


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.images = []
        self.links = []
        self.tool_count = 0
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "html":
            self.lang = attributes.get("lang")
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag == "a":
            self.links.append(attributes.get("href", ""))
        if tag == "img":
            self.images.append(attributes.get("src", ""))
        if "tool-item" in attributes.get("class", "").split():
            self.tool_count += 1


class StaticSiteTests(unittest.TestCase):
    def parse_site(self):
        parser = SiteParser()
        parser.feed(INDEX.read_text(encoding="utf-8"))
        return parser

    def test_required_files_exist(self):
        self.assertTrue(INDEX.is_file())
        self.assertTrue(STYLES.is_file())
        self.assertTrue(WORKFLOW.is_file())
        self.assertTrue(TRENDING_WORKFLOW.is_file())

    def test_page_has_required_sections_and_catalog_size(self):
        parser = self.parse_site()
        self.assertEqual(parser.lang, "zh-CN")
        self.assertTrue(REQUIRED_SECTIONS.issubset(parser.ids))
        self.assertGreaterEqual(parser.tool_count, 30)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))

    def test_links_are_nonempty_and_secure(self):
        parser = self.parse_site()
        self.assertTrue(parser.links)
        for href in parser.links:
            self.assertTrue(href)
            self.assertFalse(href.startswith("http://"))

    def test_stylesheet_is_referenced(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertIn('href="styles.css"', html)

    def test_trending_section_has_update_markers_and_source(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertEqual(html.count("GITHUB_TRENDING_START"), 1)
        self.assertEqual(html.count("GITHUB_TRENDING_END"), 1)
        self.assertIn("https://github.com/trending", html)

    def test_images_are_local_and_exist(self):
        parser = self.parse_site()
        self.assertTrue(parser.images)
        for source in parser.images:
            self.assertFalse(source.startswith("http"))
            self.assertTrue((ROOT / source).is_file(), source)

    def test_pages_workflow_uses_official_actions(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("actions/checkout@v6", workflow)
        self.assertIn("actions/configure-pages@", workflow)
        self.assertIn("actions/upload-pages-artifact@", workflow)
        self.assertIn("actions/deploy-pages@", workflow)

    def test_trending_workflow_refreshes_daily(self):
        workflow = TRENDING_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("cron: \"0 0 * * *\"", workflow)
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("contents: write", workflow)
        self.assertIn("actions/checkout@v6", workflow)
        self.assertIn("actions/setup-python@v6", workflow)
        self.assertIn("python3 scripts/update_trending.py", workflow)
        self.assertIn("git diff --quiet -- index.html", workflow)


if __name__ == "__main__":
    unittest.main()
