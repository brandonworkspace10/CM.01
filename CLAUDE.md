# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

No build step required. Deployment is via Vercel on push to main.

## Architecture

Static marketing site for an AI receptionist SaaS (Calling Matrix). No framework — all pages are self-contained HTML files with inline `<style>` and `<script>` blocks. Deployed on Vercel with two serverless API routes.

**Routing** — Vercel `cleanUrls: true` strips `.html` extensions:
- `/` → `index.html` (main landing)
- `/hvac`, `/plumbing`, `/electrical`, `/roofing`, `/cleaning` → industry-specific pages
- `/blog` → `blog/index.html`; `/blog/*` → `blog/*.html`
- `/api/contact` → `api/contact.js` (form POST, Resend email, rate limiting)
- `/api/og` → `api/og.js` (dynamic OG image, Edge runtime, `@vercel/og`)

**i18n** — Client-side EN/ES switching via `data-i18n="key"` attributes + JSON lookups in `locales/en.json` and `locales/es.json`. Language is auto-detected from the browser `Accept-Language` header on page load.

**Styling** — Each HTML file has a `<style>` block at the top defining CSS custom properties (`:root { --accent: oklch(...) }`). Industry pages vary their accent color this way.

**Analytics** — Vercel Analytics via `<script defer src="/_vercel/insights/script.js">` (served by Vercel's edge, no build step). Ahrefs tracking script also embedded inline. Both scripts are present in every page `<head>`.

## Environment Variables

| Variable | Purpose |
|---|---|
| `RESEND_API_KEY` | Transactional email via Resend (`api/contact.js`) |

Emails are sent to `callingmatrix@gmail.com`. Confirmation emails go to the lead.

## Key Patterns

- **New industry page**: Copy an existing industry page (e.g. `hvac.html`), update copy and accent color, add i18n keys to both `locales/*.json`.
- **Adding i18n strings**: Add matching keys to `locales/en.json` and `locales/es.json`, then use `data-i18n="key"` in HTML.
- **Blog posts**: Add a new `.html` file in `blog/`, link from `blog/index.html`.
- **Audio files**: Live in `/audio/`. Hero call demo uses `/audio/ai-1.mp3`, `/audio/ai-2.mp3`, `/audio/ai-3.mp3`.
- **Contact form**: Rate-limited (5/hour per IP, in-memory), honeypot field (`name="website"`), HTML-escaped before sending.
- **Structured data**: Schema.org JSON-LD embedded in `<script type="application/ld+json">` in each page `<head>`.
