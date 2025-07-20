const {chromium} = require('playwright');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const stages = [];
  for(let i=1; i<=21; i++){
    const url = `https://www.letour.fr/en/stage-${i}`;
    await page.goto(url, {waitUntil:'domcontentloaded'});
    const data = await page.evaluate(() => {
      const startEnd = document.querySelector('meta[property="og:title"]')?.content || '';
      const match = startEnd.match(/- (.*) > (.*) -/);
      const start = match ? match[1].trim() : '';
      const finish = match ? match[2].trim() : '';
      const distText = Array.from(document.querySelectorAll('td'))
        .map(td=>td.textContent.trim())
        .find(t => t.endsWith(' km'));
      const distance = distText ? parseFloat(distText) : null;
      const rows = Array.from(document.querySelectorAll('#stakes tbody tr'));
      let kom = 0, sprint = 0;
      rows.forEach(row => {
        const picto = row.querySelector('.picto');
        if(!picto) return;
        const txt = row.querySelector('td b')?.textContent || '';
        const val = parseInt(txt);
        if(isNaN(val)) return;
        if(picto.classList.contains('picto--n')) sprint += val;
        else if(picto.classList.contains('picto--a')) return;
        else kom += val;
      });
      return {start, finish, distance, kom, sprint};
    });
    stages.push({stage:i, ...data});
  }
  await browser.close();
  fs.writeFileSync('stages.json', JSON.stringify(stages, null, 2));
})();
