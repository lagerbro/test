import json, os, re, urllib.request, urllib.parse, http.cookiejar
OUT = "out"; os.makedirs(OUT, exist_ok=True)
H = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"),
     ("Origin", "https://global.novelpia.com"), ("Referer", "https://global.novelpia.com/")]
api = "https://api-global.novelpia.com"
for no in (833843, 833844):
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)); op.addheaders = H
    def get(url):
        try:
            r = op.open(url, timeout=30); return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e: return e.code, e.read().decode("utf-8", "replace")
    c, h = get(f"https://global.novelpia.com/viewer/{no}")
    print(no, "viewer", c, "cookies:", [k.name for k in cj])
    m = re.search(r'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', h)
    t = m.group(0) if m else ""
    if not t:
        c, b = get(f"{api}/v1/novel/episode?episode_no={no}")
        print(no, "episode api", c)
        try: t = json.loads(b)["result"].get("_t") or ""
        except Exception: pass
    print(no, "token:", bool(t))
    if not t: continue
    c, b = get(f"{api}/v1/novel/episode/content?_t={urllib.parse.quote(t)}")
    print(no, "content", c, b[:200] if c != 200 else "")
    open(f"{OUT}/c_{no}.json", "w").write(b)
