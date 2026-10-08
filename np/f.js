const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 2000 } });
  fs.writeFileSync('np/out.txt', '');
  await p.goto('https://global.novelpia.com/viewer/833813', { waitUntil: 'domcontentloaded', timeout: 60000 });
  for (let i = 0; i < 125; i++) {
    let t = '';
    for (let w = 0; w < 20; w++) {
      await p.waitForTimeout(1000);
      t = await p.innerText('body').catch(() => '');
      if (/Next Chapter|Author's Note/.test(t) && t.split(/\s+/).length > 300) break;
    }
    const cut = t.search(/\n\d+ Comments\n/);
    if (cut > 0) t = t.slice(0, cut);
    fs.appendFileSync('np/out.txt', `\n\n===== ${p.url()} =====\n` + t);
    try { await p.getByText('Not now').first().click({ timeout: 1500 }); } catch (e) {}
    const before = p.url();
    try { await p.getByText('Next Chapter', { exact: true }).last().click({ timeout: 8000, force: true }); } catch (e) { fs.appendFileSync('np/out.txt', '\nNEXT ERR'); break; }
    for (let w = 0; w < 15 && p.url() === before; w++) await p.waitForTimeout(1000);
    if (p.url() === before) { fs.appendFileSync('np/out.txt', '\nNO NAV'); break; }
  }
  await b.close();
})();
