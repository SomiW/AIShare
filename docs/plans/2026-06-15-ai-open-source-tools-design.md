# AI and open source developer tools site design

This document defines a static directory site for discovering AI and open
source developer tools. The site serves a broad audience, from beginners to
technical decision-makers, through clear scenario-based organization.

## Goals

The first release provides a curated, trustworthy list instead of an exhaustive
link dump. Each tool entry explains what the tool does, who it suits, its
license, and where to find the official project.

The site must:

- Deploy directly to GitHub Pages.
- Work without a build step or client-side JavaScript.
- Adapt cleanly to desktop, tablet, and mobile screens.
- Use a bright, approachable Product Hunt-inspired visual direction.
- Make contribution and source verification straightforward.

## Information architecture

The page uses a single scrolling document with four primary areas:

- A concise hero that explains the collection and links to the catalog.
- A compact category index for scanning the available scenarios.
- A curated catalog grouped by practical development scenario.
- A contribution section that links to the repository and explains the
  inclusion criteria.

The initial categories are AI coding, models and inference, agents and
automation, data and retrieval, editors and terminals, testing and quality, and
DevOps and infrastructure.

## Tool entries

Each entry contains:

- Project name.
- One-sentence purpose.
- Practical audience label.
- Open source license.
- Official repository link.
- A small set of descriptive tags.

The catalog contains approximately 30 to 40 projects in the first release.
Entries use official project repositories as the source of truth.

## Visual direction

The visual language is bright, editorial, and approachable. It uses a warm
off-white canvas, dark readable type, a saturated accent color, generous
spacing, and lightly separated tool rows or cards. The page avoids heavy
dashboard chrome and decorative complexity.

Three visual concepts will be generated after this design is approved. The
selected concept becomes the implementation target.

## Technical architecture

The site uses semantic HTML and a single CSS file. It has no framework,
package manager, external runtime dependency, or client-side behavior. A
GitHub Actions workflow publishes the repository root as a GitHub Pages
artifact.

The planned files are:

- `index.html` for page structure and curated content.
- `styles.css` for layout, typography, responsive behavior, and theme tokens.
- `.github/workflows/pages.yml` for GitHub Pages deployment.
- `README.md` for local viewing, maintenance, and deployment instructions.
- `LICENSE` for repository licensing.

## Accessibility and resilience

The page uses semantic landmarks, a logical heading structure, visible keyboard
focus, sufficient color contrast, descriptive link text, and a reduced-motion
fallback. External links remain usable when styling fails.

## Verification

Verification covers:

- HTML structure and link integrity.
- Responsive layout at common desktop and mobile widths.
- Keyboard navigation and focus visibility.
- Successful static serving from the repository root.
- GitHub Pages workflow syntax.

