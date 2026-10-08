import json, os, re, urllib.request, urllib.parse
OUT = "out"; os.makedirs(OUT, exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
     "Accept": "application/json, text/html, */*", "Origin": "https://global.novelpia.com",
     "Referer": "https://global.novelpia.com/"}
def get(name, url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=30)
        body, code = r.read().decode("utf-8", "replace"), r.status
    except urllib.error.HTTPError as e:
        body, code = e.read().decode("utf-8", "replace"), e.code
    except Exception as e:
        body, code = repr(e), -1
    open(f"{OUT}/{name}", "w").write(f"URL {url}\nHTTP {code}\n\n{body}")
    print(name, code, len(body)); return code, body
api = "https://api-global.novelpia.com"
for no in (833843, 833844, 833842, 833845):
    c, h = get(f"v_{no}.html", f"https://global.novelpia.com/viewer/{no}")
    m = re.search(r'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', h)
    print(no, "jwt:", bool(m))
    if m:
        c, b = get(f"c_{no}.json", f"{api}/v1/novel/episode/content?_t={urllib.parse.quote(m.group(0))}")
        try:
            d = json.loads(b)
            print(no, "content keys:", list((d.get("result") or {}).keys())[:10])
        except Exception as e: print("parse", e)
