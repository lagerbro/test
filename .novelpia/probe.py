import json, os, re, sys, urllib.request
OUT = "out"; os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
      "Accept": "application/json, text/html, */*", "Origin": "https://global.novelpia.com",
      "Referer": "https://global.novelpia.com/"}
def get(name, url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30)
        body = r.read().decode("utf-8", "replace"); code = r.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace"); code = e.code
    except Exception as e:
        body = repr(e); code = -1
    open(f"{OUT}/{name}", "w").write(f"URL {url}\nHTTP {code}\n\n{body}")
    print(name, code, len(body)); return code, body
N = 6589
get("novel_page.html", f"https://global.novelpia.com/novel/{N}")
api = "https://api-global.novelpia.com"
get("api_novel.json", f"{api}/v1/novel?novel_no={N}")
c, b = get("api_eplist.json", f"{api}/v1/novel/episode/list?novel_no={N}&sort=ASC&page=1&rows=50")
eps = []
try:
    d = json.loads(b)
    def walk(x):
        if isinstance(x, dict):
            if "episode_no" in x: eps.append(x)
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(d)
except Exception as e: print("parse fail", e)
print("episodes found:", len(eps))
for i, e in enumerate(eps):
    print(i+1, e.get("episode_no"), e.get("epi_num"), e.get("epi_title") or e.get("title"))
targets = [e for e in eps if str(e.get("epi_num")) in ("15", "16")] or eps[14:16]
for e in targets:
    no = e["episode_no"]
    get(f"ep_{no}_viewer.html", f"https://global.novelpia.com/viewer/{no}")
    get(f"ep_{no}_api.json", f"{api}/v1/novel/episode?episode_no={no}")
    get(f"ep_{no}_api2.json", f"{api}/v1/novel/episode/content?episode_no={no}")
