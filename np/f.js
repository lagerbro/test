const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 2000 } });
  let url = 'https://global.novelpia.com/viewer/833813';
  let out = '';
  for (let i = 0; i < 4; i++) {
    await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(e => out += 'GOTO ERR ' + e.message + '\n');
    await p.waitForTimeout(6000);
    for (let s = 0; s < 15; s++) { await p.mouse.wheel(0, 3000); await p.waitForTimeout(400); }
    const t = await p.innerText('body').catch(() => '');
    out += `\n\n===== ${url} =====\n` + t;
    const links = await p.$$eval('a', as => as.map(a => [a.innerText.trim(), a.href]));
    const ids = [...new Set(links.map(l => l[1]).filter(h => /\/viewer\/\d+/.test(h)))];
    out += '\n[viewer links] ' + ids.join(' ');
    const m = url.match(/viewer\/(\d+)/)[1];
    const next = ids.find(h => +h.match(/viewer\/(\d+)/)[1] > +m);
    if (!next) {
      const btn = p.getByText('Next Chapter', { exact: false }).first();
      try { await btn.click({ timeout: 5000 }); await p.waitForTimeout(4000); if (p.url() !== url) { url = p.url(); continue; } } catch (e) {}
      break;
    }
    url = next;
  }
  fs.writeFileSync('np/out.txt', out);
  await b.close();
})();
