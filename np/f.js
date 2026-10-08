const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 2000 } });
  let out = '';
  p.on('response', async r => { if (/episode/.test(r.url()) && /api/.test(r.url())) out += '\n[api] ' + r.url(); });
  await p.goto('https://global.novelpia.com/viewer/833813', { waitUntil: 'networkidle', timeout: 60000 });
  for (let i = 0; i < 3; i++) {
    await p.waitForTimeout(5000);
    try { await p.getByText('Not now').first().click({ timeout: 3000 }); } catch (e) {}
    const before = p.url();
    try { await p.getByText('Next Chapter', { exact: true }).last().click({ timeout: 8000, force: true }); } catch (e) { out += '\nNEXT ERR ' + e.message.split('\n')[0]; }
    await p.waitForTimeout(7000);
    try { await p.waitForLoadState('networkidle', { timeout: 20000 }); } catch (e) {}
    for (let s = 0; s < 15; s++) { await p.mouse.wheel(0, 3000); await p.waitForTimeout(300); }
    out += `\n\n===== ${before} -> ${p.url()} =====\n` + (await p.innerText('body').catch(() => ''));
    if (p.url() === before) break;
  }
  fs.writeFileSync('np/out.txt', out);
  await b.close();
})();
