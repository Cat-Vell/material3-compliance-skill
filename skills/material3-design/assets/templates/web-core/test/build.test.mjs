import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

test('shell uses semantic landmarks and labeled navigation', async () => {
  const html = await readFile(new URL('../src/index.html', import.meta.url), 'utf8');
  assert.match(html, /<main id="main"/);
  assert.match(html, /<nav aria-label="Primary"/);
  assert.match(html, /aria-current="page"/);
});

test('theme includes dark and reduced-motion paths', async () => {
  const css = await readFile(new URL('../src/tokens.css', import.meta.url), 'utf8');
  assert.match(css, /prefers-color-scheme: dark/);
  assert.match(css, /prefers-reduced-motion: reduce/);
  assert.match(css, /focus-visible/);
});
