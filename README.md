# TR3 Media Solutions

This repo is the TR3 Media Solutions agency site and Marketing That Pays funnel. It is a static HTML / CSS / JS site served on Opalstack.

## Layout

- **Root pages** — the agency site (home, services, work, case studies, contact, etc.).
- **`marketing-that-pays/`** — the MTP landing page and related funnel pages.
- **`audit.html`** (root) — the Leak Diagnosis quiz that posts to the proxy backend.
- **`advisor.html`** (root) — the AI advisor chat that posts to the proxy backend.
- **`proxy.py`** — Python backend powering the audit and advisor routes (`/api/quiz`, `/api/chat`, `/api/subscribe`).
- **`archive/`** — retired pages retained for reference.
- **`assets/`** — images and other static assets.
- **`styles.css`** — site-wide stylesheet.

## Backend

`proxy.py` runs as a long-lived Python process on the Opalstack server and listens on `127.0.0.1:$PORT`. The site's reverse proxy maps the public path `/mtp-proxy/api/*` to the local backend at `127.0.0.1:$PORT/api/*`.

## Configuration

Secrets and API keys must live in Opalstack environment variables — never in the repo. Required:

- `ANTHROPIC_API_KEY`
- `MAILCHIMP_API_KEY`
- `MAILCHIMP_LIST_ID`
- `MAILCHIMP_DC`
- `ALLOWED_ORIGIN=https://tr3mediasolutions.com`
- `PORT`
- `DB_PATH` (optional — absolute path to the SQLite file)

## Deployment

Deployment is manual through the Opalstack site / app workflow: upload changed files via SSH or SFTP, restart the proxy app from the Opalstack control panel when `proxy.py` changes, and confirm via the standard end-to-end check on `https://tr3mediasolutions.com/mtp-proxy/api/quiz`.
