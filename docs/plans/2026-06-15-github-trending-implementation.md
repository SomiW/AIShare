# GitHub Trending daily section implementation plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to
> implement this plan task-by-task.

**Goal:** Add two five-item GitHub Trending lists that refresh every day at
08:00 Asia/Shanghai and deploy as static HTML.

**Architecture:** A Python standard-library generator fetches and parses GitHub
Trending pages, classifies repositories, and replaces a marker-delimited
section in `index.html`. A scheduled GitHub Actions workflow runs the generator,
commits changed content, and lets the existing Pages workflow deploy it.

**Tech Stack:** HTML, CSS, Python 3 standard library, `unittest`, GitHub Actions.

---

### Task 1: Parse and classify trending repositories

**Files:**
- Create: `scripts/update_trending.py`
- Create: `tests/fixtures/github-trending.html`
- Create: `tests/test_trending.py`

**Step 1: Write the failing parser tests**

Add tests that load the fixture and assert repository name, URL, description,
language, total stars, and stars gained today. Add tests that deduplicate
repositories and classify AI-related descriptions.

**Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests/test_trending.py -v`

Expected: FAIL because `scripts.update_trending` doesn't exist.

**Step 3: Implement the parser and classifier**

Use `html.parser.HTMLParser` to parse `article.Box-row` cards. Normalize
whitespace, convert star counts to integers, deduplicate by repository name,
and match a focused list of AI keywords against repository names and
descriptions.

**Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests/test_trending.py -v`

Expected: all parser and classifier tests pass.

**Step 5: Commit**

```bash
git add scripts/update_trending.py tests/fixtures/github-trending.html \
  tests/test_trending.py
git commit -m "feat: parse GitHub Trending repositories"
```

### Task 2: Render and update the static section

**Files:**
- Modify: `scripts/update_trending.py`
- Modify: `tests/test_trending.py`
- Modify: `index.html`
- Modify: `styles.css`
- Modify: `tests/test_site.py`

**Step 1: Write failing rendering tests**

Add tests that assert the rendered HTML contains two ranked lists, escaped
descriptions, metadata, source attribution, and a generated date. Add a marker
replacement test and static-site assertions for the `trending` section.

**Step 2: Run tests to verify they fail**

Run:
`python3 -m unittest tests/test_trending.py tests/test_site.py -v`

Expected: FAIL because the renderer, markers, and section don't exist.

**Step 3: Implement rendering and page styles**

Add stable `GITHUB_TRENDING_START` and `GITHUB_TRENDING_END` comments to
`index.html`. Render five AI entries and five non-AI development entries.
Create a responsive two-column editorial layout in `styles.css`.

**Step 4: Run tests to verify they pass**

Run:
`python3 -m unittest tests/test_trending.py tests/test_site.py -v`

Expected: all tests pass.

**Step 5: Commit**

```bash
git add scripts/update_trending.py tests/test_trending.py tests/test_site.py \
  index.html styles.css
git commit -m "feat: add daily trending section"
```

### Task 3: Schedule daily refreshes

**Files:**
- Create: `.github/workflows/update-trending.yml`
- Modify: `tests/test_site.py`
- Modify: `README.md`

**Step 1: Write failing workflow tests**

Assert that the workflow has a `0 0 * * *` schedule, manual dispatch, contents
write permission, Python setup, generator execution, and a guarded commit.

**Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests/test_site.py -v`

Expected: FAIL because the scheduled workflow doesn't exist.

**Step 3: Add the workflow and documentation**

Run the updater daily and manually. Commit only when `index.html` changes, using
the GitHub Actions bot identity. Document the generated section and manual
refresh command.

**Step 4: Run full verification**

Run:

```bash
python3 -m unittest discover -s tests -v
ruby -e 'require "yaml"; Dir[".github/workflows/*.yml"].each { |f| YAML.safe_load(File.read(f), aliases: true) }; puts "workflow yaml: ok"'
git diff --check
```

Expected: all tests pass, YAML parses, and `git diff --check` exits cleanly.

**Step 5: Commit**

```bash
git add .github/workflows/update-trending.yml tests/test_site.py README.md
git commit -m "ci: refresh GitHub Trending every day"
```

### Task 4: Validate live data and deploy

**Files:**
- Modify: `index.html`

**Step 1: Run the updater against GitHub Trending**

Run: `python3 scripts/update_trending.py`

Expected: `index.html` contains current daily trending repositories.

**Step 2: Run full verification again**

Run the full test, YAML, and diff checks from Task 3.

**Step 3: Inspect desktop and mobile layouts**

Open the local site in the in-app browser. Confirm both lists are readable at
desktop and mobile widths and that all repository links work.

**Step 4: Commit generated content**

```bash
git add index.html
git commit -m "data: update daily GitHub Trending"
```

**Step 5: Push and verify Pages**

Push `master`, wait for both Actions workflows, and verify the published page
and its stylesheet return HTTP 200.

