# GitHub Trending daily section design

The site will add a daily trending section sourced from GitHub Trending. A
scheduled GitHub Actions workflow will refresh the section every day at 08:00
Asia/Shanghai time and redeploy the static site.

## Product behavior

The section appears between the hero and editor's picks. It contains two lists:

- **AI 热门**: Five repositories whose names or descriptions match AI-related
  terms.
- **开发热门**: Five repositories from the same daily trending results after
  excluding the AI list.

Each entry displays its rank, repository name, description, primary language,
and stars gained today. The section also displays the generated date and links
to GitHub Trending as its source.

Desktop layouts show the two lists side by side. Mobile layouts stack the lists.
The visual treatment follows the site's existing editorial cards, colors,
typography, and spacing.

## Data flow

A Python script fetches GitHub Trending daily pages and parses repository cards.
It combines and deduplicates results, classifies repositories, and renders a
static HTML fragment between stable marker comments in `index.html`.

The scheduled workflow runs at `00:00 UTC`, which is 08:00 in Asia/Shanghai. It
also supports manual dispatch. When generated content changes, the workflow
commits `index.html` back to the repository. The existing Pages workflow then
deploys the new commit.

GitHub Trending doesn't provide a supported public API. The parser therefore
uses the public HTML page and keeps its selectors isolated in one module.

## Reliability

The updater validates that it found repository cards before editing the site.
If fetching or parsing fails, it exits with an error and leaves the last
successful daily list unchanged.

If fewer than five matching repositories exist, the page shows the available
items instead of filling the list with unrelated projects. Repository
descriptions are escaped before they are added to HTML.

## Testing

Unit tests use a saved, minimal HTML fixture rather than the network. Tests
cover parsing, deduplication, AI classification, HTML escaping, section
rendering, and marker replacement. Existing static-site tests verify the new
section and both workflows.

