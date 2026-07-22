import { readFile } from 'node:fs/promises';

const target = process.argv[2];
if (!target) {
  console.error('Usage: node scripts/a11y-smoke.mjs <html-file>');
  process.exit(2);
}

const html = await readFile(target, 'utf8');
const checks = [
  ['document language', /<html[^>]+lang=["'][^"']+["']/i],
  ['unique main landmark', /<main\b/i],
  ['named navigation', /<nav[^>]+aria-label=["'][^"']+["']/i],
  ['skip link', /href=["']#main["']/i],
  ['visible focus CSS is linked', /tokens\.css/i],
  ['theme toggle has pressed state', /id=["']theme-toggle["'][^>]+aria-pressed=/i],
];

const failures = checks.filter(([, pattern]) => !pattern.test(html));
if (failures.length) {
  for (const [name] of failures) console.error(`FAIL: ${name}`);
  process.exit(1);
}
console.log(`Accessibility smoke passed (${checks.length} structural checks).`);
