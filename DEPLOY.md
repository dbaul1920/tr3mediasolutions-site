# Deploy Instructions — Marketing That Pays™
## File structure on your server

```
/home/yourusername/
  mtp-proxy/
    proxy.py          ← the proxy server
    start-proxy.sh    ← startup script

public_html/
  marketing-that-pays/
    index.html        ← landing page
    audit.html        ← audit tool
    advisor.html      ← AI advisor (updated to use proxy)
```

---

## Step 1 — Upload the HTML files

Upload `index.html`, `audit.html`, and `advisor.html` to:
```
public_html/marketing-that-pays/
```

---

## Step 2 — Set up the proxy on Opalstack

1. Log into your Opalstack control panel
2. Go to **Apps** → **Add App**
3. Choose **Custom Python App** (or **Shell App** if Python app isn't listed)
4. Set the port — use **8080** (or whatever Opalstack assigns)
5. Upload `proxy.py` to the app directory Opalstack creates for you
6. In the app's **Environment Variables**, add:
   ```
   ANTHROPIC_API_KEY = sk-ant-your-key-here
   ALLOWED_ORIGIN = https://tr3mediasolutions.com
   PORT = 8080
   ```
7. Set the **Startup command** to: `python3 proxy.py`
8. Start the app

---

## Step 3 — Point advisor.html at the proxy

Once Opalstack gives you the internal URL for your custom app (something like `https://tr3mediasolutions.com/mtp-proxy` or a port URL), open `advisor.html` and find this line:

```javascript
const PROXY_URL = 'https://tr3mediasolutions.com/mtp-proxy/api/chat';
```

Replace with whatever URL Opalstack assigned. Save and re-upload.

---

## Step 4 — Get your Anthropic API key

1. Go to console.anthropic.com
2. Click **API Keys** → **Create Key**
3. Copy it — you only see it once
4. Paste it into the Opalstack environment variable

---

## Step 5 — Test it

1. Visit `https://tr3mediasolutions.com/marketing-that-pays/advisor.html`
2. Send a message
3. You should get a response within 5–10 seconds

If it doesn't work, check:
- Is the proxy app running? (Opalstack dashboard → Apps → Status)
- Is the API key set correctly? (no extra spaces)
- Is the PROXY_URL in advisor.html pointing to the right address?

---

## Ongoing cost

The Claude API charges per token. At typical conversation length (5–10 exchanges), each advisor session costs roughly $0.01–0.03. For 100 sessions/month that's $1–3. Not worth worrying about until you're getting significant traffic.

---

## If you get stuck

The proxy is plain Python — no dependencies, no packages to install. If Opalstack support asks what it is, tell them: "A simple HTTP server that proxies requests to an external API." That's exactly what it is.
