/* Dependency-free browser smoke test via the Chrome DevTools Protocol. */
import { writeFile } from 'node:fs/promises';

const port = process.argv[2] || '9222';
const screenshotPath = process.argv[3];
const origin = `http://127.0.0.1:${port}`;
const targetUrl = process.argv[4] || 'http://127.0.0.1:4173/';
const detailScreenshotPath = process.argv[5];
const desktopScreenshotPath = process.argv[6];
const mobileDetailScreenshotPath = process.argv[7];

const targetResponse = await fetch(`${origin}/json/new?${encodeURIComponent(targetUrl)}`, { method: 'PUT' });
if (!targetResponse.ok) throw new Error(`Cannot create browser target: ${targetResponse.status}`);
const target = await targetResponse.json();
const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  socket.addEventListener('open', resolve, { once: true });
  socket.addEventListener('error', reject, { once: true });
});

let nextId = 1;
const waiting = new Map();
socket.addEventListener('message', event => {
  const message = JSON.parse(event.data);
  if (!message.id || !waiting.has(message.id)) return;
  const { resolve, reject } = waiting.get(message.id);
  waiting.delete(message.id);
  if (message.error) reject(new Error(message.error.message));
  else resolve(message.result);
});

function send(method, params = {}) {
  const id = nextId++;
  socket.send(JSON.stringify({ id, method, params }));
  return new Promise((resolve, reject) => waiting.set(id, { resolve, reject }));
}
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
async function evaluate(expression) {
  const response = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (response.exceptionDetails) throw new Error(response.exceptionDetails.text);
  return response.result.value;
}
function assert(condition, message) {
  if (!condition) throw new Error(`Browser assertion failed: ${message}`);
  console.log(`PASS: ${message}`);
}

await send('Page.enable');
await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
await sleep(1800);
await evaluate(`localStorage.clear()`);
await send('Page.reload', { ignoreCache: true });
for (let attempt = 0; attempt < 40; attempt += 1) {
  const ready = await evaluate(`document.readyState === 'complete' && document.querySelectorAll('.problem-card').length === 100`);
  if (ready) break;
  await sleep(200);
}

const initial = await evaluate(`({
  ready: document.readyState,
  data: window.HOT100_PROBLEMS?.length,
  enriched: window.HOT100_PROBLEMS?.filter(p => p.statement && p.examples?.length && p.constraints?.length && Array.isArray(p.api_notes)).length,
  cards: document.querySelectorAll('.problem-card').length,
  title: document.title,
  layout: document.documentElement.dataset.layout,
  desktopNav: getComputedStyle(document.querySelector('.desktop-nav')).display,
  mobileNav: getComputedStyle(document.querySelector('.mobile-tabbar')).display,
  listColumns: getComputedStyle(document.querySelector('.problem-list')).gridTemplateColumns
})`);
assert(initial.ready === 'complete', 'page completed loading');
assert(initial.data === 100 && initial.cards === 100, '100 data records render as 100 cards');
assert(initial.enriched === 100, 'all 100 records include statements, examples, constraints, and API-note data');
assert(initial.title.includes('HOT 100'), 'document metadata is present');
assert(initial.layout === 'desktop' && initial.desktopNav !== 'none' && initial.mobileNav === 'none', 'desktop layout exposes desktop navigation and hides mobile navigation');
assert(initial.listColumns.trim().split(/\s+/).length === 2, `desktop layout renders a two-column problem list (${initial.listColumns})`);
if (desktopScreenshotPath) {
  const screenshot = await send('Page.captureScreenshot', { format: 'png', fromSurface: true });
  await writeFile(desktopScreenshotPath, Buffer.from(screenshot.data, 'base64'));
  console.log(`PASS: wrote desktop screenshot to ${desktopScreenshotPath}`);
}

const detail = await evaluate(`(() => {
  document.querySelector('.problem-card[data-id="1"]').click();
  return {
    open: document.querySelector('#problem-dialog').open,
    text: document.querySelector('#problem-detail').innerText,
    allText: document.querySelector('#problem-detail').textContent,
    formula: document.querySelectorAll('#problem-detail .katex').length,
    statementColumns: getComputedStyle(document.querySelector('.statement-body')).gridTemplateColumns
  };
})()`);
assert(detail.open && detail.text.includes('两数之和') && detail.text.includes('Python 3'), 'problem detail dialog opens with explanation and code');
assert(detail.text.includes('完整题目与输入输出') && detail.text.includes('示例 1') && detail.text.includes('数据范围与约束'), 'problem detail includes the complete statement, examples, and constraints');
assert(detail.allText.includes('Python 函数 / 方法') && detail.allText.includes('enumerate'), 'problem detail explains Python APIs used by the solution');
assert(detail.formula > 0, 'KaTeX rendered the problem formula');
assert(detail.statementColumns.trim().split(/\s+/).length === 2, `desktop detail uses a two-column statement layout (${detail.statementColumns})`);
if (detailScreenshotPath) {
  await evaluate(`document.querySelector('.statement-card').scrollIntoView({ block: 'start' })`);
  await sleep(250);
  const screenshot = await send('Page.captureScreenshot', { format: 'png', fromSurface: true });
  await writeFile(detailScreenshotPath, Buffer.from(screenshot.data, 'base64'));
  console.log(`PASS: wrote detail screenshot to ${detailScreenshotPath}`);
}

const progress = await evaluate(`(() => {
  document.querySelector('#mark-done').click();
  const saved = JSON.parse(localStorage.getItem('hot100-study-v1'));
  return { done: saved.done, count: document.querySelector('#done-count').textContent };
})()`);
assert(progress.done.includes('1') && progress.count === '1', 'completion state persists in localStorage and updates progress');

await evaluate(`document.querySelector('#dialog-close').click()`);
const search = await evaluate(`(() => {
  const input = document.querySelector('#search-input');
  input.value = '最小栈';
  input.dispatchEvent(new Event('input', { bubbles: true }));
  return { cards: document.querySelectorAll('.problem-card').length, text: document.querySelector('.problem-card')?.innerText };
})()`);
assert(search.cards === 1 && search.text.includes('155'), 'full-text search filters to the expected problem');

await evaluate(`document.querySelector('#clear-filters').click()`);
const hard = await evaluate(`(() => {
  document.querySelector('[data-difficulty="HARD"]').click();
  return document.querySelectorAll('.problem-card').length;
})()`);
assert(hard === 12, 'difficulty filter returns all 12 hard problems');

const linked = await evaluate(`(() => {
  document.querySelector('[data-difficulty="ALL"]').click();
  [...document.querySelectorAll('[data-category]')].find(x => x.dataset.category === '链表').click();
  return document.querySelectorAll('.problem-card').length;
})()`);
assert(linked === 14, 'category navigation returns all 14 linked-list problems');

const theme = await evaluate(`(() => {
  const before = document.documentElement.dataset.theme;
  document.querySelector('#theme-button').click();
  return { before, after: document.documentElement.dataset.theme };
})()`);
assert(theme.before !== theme.after, 'theme toggle updates the document theme');

await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
await send('Page.reload', { ignoreCache: true });
for (let attempt = 0; attempt < 40; attempt += 1) {
  const ready = await evaluate(`document.readyState === 'complete' && document.documentElement.dataset.layout === 'mobile' && document.querySelectorAll('.problem-card').length === 100`);
  if (ready) break;
  await sleep(200);
}
await evaluate(`window.scrollTo(0, 0)`);
const mobile = await evaluate(`(() => ({
  clientWidth: document.documentElement.clientWidth,
  scrollWidth: document.documentElement.scrollWidth,
  layout: document.documentElement.dataset.layout,
  desktopNav: getComputedStyle(document.querySelector('.desktop-nav')).display,
  mobileNav: getComputedStyle(document.querySelector('.mobile-tabbar')).display,
  mobileProgress: getComputedStyle(document.querySelector('#mobile-progress-button')).display,
  tabHeight: Math.round(document.querySelector('.mobile-tabbar button').getBoundingClientRect().height),
  offenders: [...document.querySelectorAll('body *')]
    .map(el => ({ name: el.tagName + '.' + el.className, right: Math.round(el.getBoundingClientRect().right), width: Math.round(el.getBoundingClientRect().width) }))
    .filter(x => x.right > document.documentElement.clientWidth + 1)
    .slice(0, 8)
}))()`);
assert(mobile.layout === 'mobile' && mobile.desktopNav === 'none' && mobile.mobileNav !== 'none' && mobile.mobileProgress !== 'none', 'mobile layout exposes mobile controls and hides desktop navigation');
assert(mobile.tabHeight >= 44, `mobile navigation provides touch-friendly targets (${mobile.tabHeight}px)`);
assert(mobile.scrollWidth <= mobile.clientWidth + 1, `mobile layout has no horizontal overflow (${JSON.stringify(mobile)})`);
if (screenshotPath) {
  const screenshot = await send('Page.captureScreenshot', { format: 'png', fromSurface: true });
  await writeFile(screenshotPath, Buffer.from(screenshot.data, 'base64'));
  console.log(`PASS: wrote mobile screenshot to ${screenshotPath}`);
}
const mobileDetail = await evaluate(`(() => {
  document.querySelector('.problem-card[data-id="1"]').click();
  return {
    open: document.querySelector('#problem-dialog').open,
    statementColumns: getComputedStyle(document.querySelector('.statement-body')).gridTemplateColumns,
    footerDisplay: getComputedStyle(document.querySelector('.dialog-footer')).display
  };
})()`);
assert(mobileDetail.open && mobileDetail.statementColumns.trim().split(/\s+/).length === 1, `mobile detail collapses statement content to one column (${mobileDetail.statementColumns})`);
assert(mobileDetail.footerDisplay === 'grid', 'mobile detail uses the dedicated grid action footer');
if (mobileDetailScreenshotPath) {
  await evaluate(`document.querySelector('.statement-card').scrollIntoView({ block: 'start' })`);
  await sleep(250);
  const screenshot = await send('Page.captureScreenshot', { format: 'png', fromSurface: true });
  await writeFile(mobileDetailScreenshotPath, Buffer.from(screenshot.data, 'base64'));
  console.log(`PASS: wrote mobile detail screenshot to ${mobileDetailScreenshotPath}`);
}

await fetch(`${origin}/json/close/${target.id}`);
socket.close();
console.log('PASS: browser interaction smoke test completed');

