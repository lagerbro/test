import os, re, urllib.request
OUT = "out"; os.makedirs(OUT, exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=30).read().decode("utf-8", "replace")
h = fetch("https://global.novelpia.com/viewer/833843")
js = sorted(set(re.findall(r'/_nuxt/[A-Za-z0-9_.-]+\.js', h)))
seen, queue, snips = set(), list(js), []
while queue and len(seen) < 300:
    p = queue.pop()
    if p in seen: continue
    seen.add(p)
    try: s = fetch("https://global.novelpia.com" + p)
    except Exception as e: continue
    for q in re.findall(r'["\'/(]([A-Za-z0-9_.-]+\.js)["\']', s):
        if ("/_nuxt/" + q) not in seen and len(q) < 40: queue.append("/_nuxt/" + q)
    for kw in ("episode/content", "pv-gn", "signed_key", "CloudFront", "_t"):
        for m in re.finditer(re.escape(kw), s):
            if kw == "_t" and not re.match(r'_t\b', s[m.start():m.start()+3]): continue
            snips.append(f"### {p} [{kw}]\n{s[max(0,m.start()-600):m.start()+900]}\n")
            if kw == "_t" and len(snips) > 80: break
print("files scanned", len(seen), "snips", len(snips))
open(f"{OUT}/snips.txt", "w").write("\n".join(snips))
