# TR3 Media Solutions — Website Prototype

Static HTML/CSS prototype for the TR3 Media Solutions website. Designed for review and eventual translation into a Divi WordPress theme.

## How to Open

1. Navigate to the `site-prototype/` folder
2. Double-click `index.html` to open in any modern browser
3. Navigate between pages using the header/footer links

No server, build step, or dependencies required. Everything runs from the local file system.

## File Structure

```
site-prototype/
├── index.html                          # Home page
├── about.html                          # About page
├── services.html                       # Services page
├── work.html                           # Work/portfolio page
├── case-study.html                     # Case study template (sample content)
├── how-we-work.html                    # How We Work page
├── insights.html                       # Insights/blog listing
├── insight-detail.html                 # Insight article template (sample content)
├── start.html                          # Project inquiry form
├── start-confirmation-retainer.html    # Confirmation: retainer-qualified path
├── start-confirmation-project.html     # Confirmation: project-qualified path
├── start-confirmation-decline.html     # Confirmation: decline path
├── contact.html                        # Contact page
├── privacy.html                        # Privacy policy
├── terms.html                          # Terms of use
├── accessibility.html                  # Accessibility statement
├── styles.css                          # All styles (single file)
├── README.md                           # This file
└── assets/
    ├── logos/
    │   ├── tr3-logo-green.png          # Primary logo (header use)
    │   ├── tr3-logo-white.png          # White logo (footer/dark bg)
    │   └── tr3-logo-white.svg          # SVG version of white logo
    └── images/
        ├── hero-team.jpg               # Team collaboration photo
        ├── about-team.jpg              # About page team photo
        ├── founder.jpg                 # Founder portrait
        ├── services-hero.jpg           # Services imagery
        ├── work-hero.jpg               # Work page imagery
        ├── how-we-work.jpg             # How We Work imagery
        ├── insights-hero.jpg           # Insights imagery
        └── case-study-sample.jpg       # Sample case study image
```

## Routing Prototype (Intake Form)

The `start.html` page contains the full project inquiry form. Since this is a static prototype with no backend, form routing is simulated.

### Default Behavior (Option A — No JS Required)

The form displays three labeled submit buttons at the bottom:

- **Submit (Prototype: Retainer Qualified)** → `start-confirmation-retainer.html`
- **Submit (Prototype: Project Qualified)** → `start-confirmation-project.html`
- **Submit (Prototype: Decline)** → `start-confirmation-decline.html`

Click any button to preview that confirmation flow. This allows stakeholders to review all three paths without filling out the form.

### Optional JS Routing (Option B)

The `start.html` file contains commented-out JavaScript at the bottom that implements client-side routing logic. To activate:

1. Open `start.html` in a text editor
2. Find the comment block starting with `// Option B: JS-based routing`
3. Uncomment the IIFE block (remove `/*` and `*/`)
4. Save and reload

When active, the three prototype buttons are hidden and replaced with a single "Submit Inquiry" button. The JS evaluates form selections and redirects to the appropriate confirmation page using these rules:

**Retainer Path** (all must be true):
- Organization type: Nonprofit/Foundation, Public Sector/Education, or Social Impact Business
- Support includes "Ongoing creative partnership" OR multiple support types selected
- Investment: $10k–$25k or $25k+
- Funding: Yes or In progress
- Working style: Strategic partner

**Project Path** (all must be true):
- Decision-maker: Yes or Closely involved
- Support includes at least one of: Website, Campaign, Brand, Print
- Investment: $5k–$10k or $10k–$25k
- Funding: Yes or In progress
- Working style: Strategic partner or Execution with guidance

**Decline Path** (any one triggers decline):
- Investment: Under $5,000
- Funding: Not yet
- Decision-maker: No
- Working style: Production only
- Timeframe "Exploring" + Investment under $10k
- "Why TR3" answer empty or under 25 characters

### Calendar Gate

The scheduling link appears ONLY on `start-confirmation-retainer.html`. It is not present anywhere else on the site. In production, replace the `#` placeholder href with the actual scheduling URL.

## Conditional Form Notes

Two form fields display contextual notes:

- **Decision-maker = "No"** shows: "We prioritize projects with clear decision-making authority."
- **Funding = "Not yet"** shows: "We typically engage once funding and internal readiness are confirmed."

These use minimal inline JS (event listeners on radio buttons) and work without the Option B routing code.

## Design System

### Colors
- Primary green: `#2D5A27`
- Hover green: `#1E3E1B`
- Light green (accents): `#E8F0E6`
- Body text: `#2C2C2C`
- Secondary text: `#6B6B6B`
- Background tint: `#F7F6F3`

### Typography
- Headings: Georgia (serif)
- Body: System font stack (-apple-system, etc.)
- Base size: 16px (1rem)

### Breakpoints
- Desktop: > 1024px
- Tablet: 769px–1024px
- Mobile: ≤ 768px
- Small mobile: ≤ 480px

## Notes for Divi Translation

### Section → Divi Mapping

| Prototype Element | Divi Module |
|---|---|
| `.hero` | Fullwidth Header module or custom Section |
| `.section` | Regular Section |
| `.section--tinted` | Section with background color `#F7F6F3` |
| `.section--green` | Section with background color `#2D5A27` |
| `.container` | Row (max-width 1200px, centered) |
| `.grid--2` | Row with 2 columns (1/2 + 1/2) |
| `.grid--3` | Row with 3 columns (1/3 + 1/3 + 1/3) |
| `.grid--4` | Row with 4 columns (1/4 each) |
| `.split` | Row with 2 columns (text + image) |
| `.pillar-card` | Blurb module with left border |
| `.work-card` | Blog module or custom portfolio grid |
| `.btn--primary` | Button module (green background) |
| `.btn--secondary` | Button module (outlined/green border) |
| `.service-block` | Text module inside Section with bottom divider |
| `.cta-banner` | CTA module or Section with centered Text + Button |
| `.form-section` | Contact Form 7 or Gravity Forms + custom CSS |
| `.principles-list` | Text module with styled list |
| `.content-block` | Text module |
| `.site-footer` | Global Footer (Section with dark background) |

### General Translation Notes

1. **Header**: Use Divi Theme Builder global header. Logo left, menu right, CTA button as menu item.
2. **Footer**: Use Divi Theme Builder global footer. Three-column layout on dark background.
3. **Forms**: The intake form is complex. Consider Gravity Forms with conditional logic for the routing rules. The form sections map to Gravity Forms field groups.
4. **Confirmation pages**: Can be separate WordPress pages or handled via Gravity Forms confirmation routing.
5. **CSS Variables**: Divi uses its own variable system. Transfer color values to Divi's Theme Customizer.
6. **Responsive**: Divi handles responsive automatically, but review breakpoints in Divi's responsive editing mode.
7. **Typography**: Set Georgia as the heading font and system fonts as body in Divi's Theme Customizer > Typography.
8. **Spacing**: The prototype uses generous whitespace (6rem–8rem section padding). Maintain this in Divi with custom padding on Sections.

## Swapping in Real Content

### Case Studies
- Replace the three placeholder case studies in `work.html` with real project data
- Duplicate `case-study.html` for each real case study, updating content and metadata
- Replace placeholder images in `assets/images/`

### Images
- Replace stock photos with branded photography or project screenshots
- Maintain aspect ratios (16:10 for work cards, 4:3 for split layouts)
- Optimize images for web (recommended: WebP format, max 1600px wide)

### Insights
- Replace sample articles in `insights.html` with real content
- Duplicate `insight-detail.html` template for each article

### Logo
- Current logos are PNG. For production, consider SVG versions for crisp rendering at all sizes.
