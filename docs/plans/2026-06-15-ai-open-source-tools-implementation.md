# AI and Open Source Developer Tools Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to
> implement this plan task-by-task.

**Goal:** Build a curated, responsive, zero-build tools directory that deploys
to GitHub Pages.

**Architecture:** Use one semantic HTML document and one CSS stylesheet. Keep
all catalog content in HTML so the page works without JavaScript, then publish
the repository root through the official GitHub Pages Actions flow.

**Tech Stack:** HTML5, CSS3, GitHub Actions, GitHub Pages

---

### Task 1: Select the visual target

**Files:**

- Reference:
  `docs/plans/2026-06-15-ai-open-source-tools-design.md`

**Step 1: Generate three independent concepts**

Create three desktop, scrollable visual concepts based on the approved design
brief.

**Step 2: Present the concepts**

Give each concept a short name and explain its key hierarchy and visual choices.

**Step 3: Record the selection**

Use the selected concept as the visual target for implementation.

### Task 2: Research and curate the catalog

**Files:**

- Create: `index.html`

**Step 1: Gather candidate projects**

Collect official repositories for approximately 30 to 40 tools across the
approved categories.

**Step 2: Verify project metadata**

Confirm each project's purpose, official repository URL, and license from
primary sources.

**Step 3: Draft concise entries**

Write one-sentence descriptions and audience labels in consistent Chinese.

### Task 3: Build the semantic page

**Files:**

- Create: `index.html`

**Step 1: Add document metadata**

Add the language, viewport, description, social preview metadata, and stylesheet
reference.

**Step 2: Add the page landmarks**

Create the header, main content, catalog sections, contribution section, and
footer.

**Step 3: Add the curated entries**

Render every verified tool using consistent semantic markup.

**Step 4: Check the unstyled document**

Run:

```bash
python3 -m http.server 8000
```

Expected: The full catalog is readable at `http://localhost:8000`.

### Task 4: Implement the selected visual direction

**Files:**

- Create: `styles.css`
- Modify: `index.html`

**Step 1: Define design tokens**

Add custom properties for color, typography, spacing, borders, and layout.

**Step 2: Style global structure**

Implement the canvas, header, hero, category index, catalog groups, and footer.

**Step 3: Style tool entries**

Match the selected concept's hierarchy, density, labels, and link treatment.

**Step 4: Add responsive behavior**

Test at 1440, 1024, 768, and 390 CSS pixels.

**Step 5: Add accessibility states**

Implement visible focus styles, readable contrast, and reduced-motion behavior.

### Task 5: Configure GitHub Pages

**Files:**

- Create: `.github/workflows/pages.yml`
- Create: `.nojekyll`

**Step 1: Add the deployment workflow**

Use the official Pages configuration, artifact upload, and deployment actions.

**Step 2: Validate the YAML**

Parse the workflow with an available YAML parser.

Expected: The file parses without errors.

### Task 6: Document maintenance and deployment

**Files:**

- Create: `README.md`
- Create: `LICENSE`

**Step 1: Document local viewing**

Explain how to serve the repository with Python's static HTTP server.

**Step 2: Document GitHub Pages setup**

Explain the repository setting required to use GitHub Actions as the Pages
source.

**Step 3: Document contribution criteria**

Explain how projects are selected and what metadata a contribution must include.

### Task 7: Verify the finished site

**Files:**

- Test: `index.html`
- Test: `styles.css`
- Test: `.github/workflows/pages.yml`

**Step 1: Run static checks**

Check for missing local files, duplicate IDs, empty links, and malformed markup.

**Step 2: Inspect the rendered page**

Serve the site locally and inspect desktop and mobile layouts in the configured
browser.

**Step 3: Check external links**

Verify that every project link points to an official repository.

**Step 4: Review the final diff**

Run:

```bash
git diff --check
git status --short
```

Expected: No whitespace errors, and only intended project files are changed.

