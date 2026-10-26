(() => {
  'use strict';
  const problems = window.HOT100_PROBLEMS || [];
  const categories = [...new Set(problems.map(p => p.category))];
  const STORE_KEY = 'hot100-study-v1';
  const state = {
    query: '', status: 'all', difficulty: 'ALL', category: '全部专题',
    currentId: null, studyMode: false,
    saved: loadSaved()
  };
  const $ = s => document.querySelector(s);
  const els = {
    list: $('#problem-list'), empty: $('#empty-state'), search: $('#search-input'),
    categoryNav: $('#category-nav'), resultCount: $('#result-count'),
    activeFilters: $('#active-filters'), dialog: $('#problem-dialog'),
    detail: $('#problem-detail'), doneCount: $('#done-count'), ring: $('#progress-ring'),
    lineFill: $('#progress-line-fill'), caption: $('#progress-caption'),
    continueBtn: $('#continue-button'), markDone: $('#mark-done'), favorite: $('#dialog-favorite'),
    prev: $('#prev-problem'), next: $('#next-problem'), toast: $('#toast')
  };

  function loadSaved() {
    try {
      return JSON.parse(localStorage.getItem(STORE_KEY)) || { done: [], favorites: [], recent: null, theme: 'light' };
    } catch (_) {
      return { done: [], favorites: [], recent: null, theme: 'light' };
    }
  }
  function persist() { localStorage.setItem(STORE_KEY, JSON.stringify(state.saved)); }
  const isDone = id => state.saved.done.includes(String(id));
  const isFavorite = id => state.saved.favorites.includes(String(id));
  function toggleIn(list, id, force) {
    id = String(id); const has = list.includes(id); const should = force === undefined ? !has : force;
    if (should && !has) list.push(id); else if (!should && has) list.splice(list.indexOf(id), 1);
    persist(); updateProgress(); renderList(); return should;
  }
  function escapeHtml(value='') { return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c])); }
  function highlightPython(code) {
    const tokenPattern = /#[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\b(?:class|def|return|if|else|elif|for|while|in|not|and|or|is|None|True|False|from|import|as|pass|break|continue|nonlocal)\b|\b\d+(?:\.\d+)?\b/g;
    let html = '';
    let last = 0;
    for (const match of code.matchAll(tokenPattern)) {
      html += escapeHtml(code.slice(last, match.index));
      const token = match[0];
      const kind = token.startsWith('#') ? 'comment'
        : token.startsWith('"') || token.startsWith("'") ? 'string'
        : /^\d/.test(token) ? 'number' : 'keyword';
      html += `<span class="token-${kind}">${escapeHtml(token)}</span>`;
      last = match.index + token.length;
    }
    return html + escapeHtml(code.slice(last));
  }
  function difficultyLabel(d) { return { EASY: '简单', MEDIUM: '中等', HARD: '困难' }[d] || d; }
  function difficultyClass(d) { return d.toLowerCase(); }
  function matches(p) {
    const haystack = `${p.id} ${p.title} ${p.slug} ${p.category} ${(p.tags || []).join(' ')} ${p.signal} ${p.summary}`.toLowerCase();
    const queryOK = !state.query || haystack.includes(state.query.toLowerCase());
    const difficultyOK = state.difficulty === 'ALL' || p.difficulty === state.difficulty;
    const categoryOK = state.category === '全部专题' || p.category === state.category;
    const statusOK = state.status === 'all' || (state.status === 'done' && isDone(p.id)) ||
      (state.status === 'todo' && !isDone(p.id)) || (state.status === 'favorite' && isFavorite(p.id));
    return queryOK && difficultyOK && categoryOK && statusOK;
  }
  function renderCategoryNav() {
    const items = ['全部专题', ...categories];
    els.categoryNav.innerHTML = items.map(name => {
      const count = name === '全部专题' ? problems.length : problems.filter(p => p.category === name).length;
      return `<button type="button" class="${state.category === name ? 'active' : ''}" data-category="${escapeHtml(name)}"><span>${escapeHtml(name)}</span><small>${count}</small></button>`;
    }).join('');
  }
  function renderList() {
    const visible = problems.filter(matches);
    els.resultCount.textContent = `显示 ${visible.length} 道`;
    els.empty.hidden = visible.length > 0;
    els.list.hidden = visible.length === 0;
    els.list.innerHTML = visible.map((p) => `
      <article class="problem-card ${isDone(p.id) ? 'done' : ''}" data-id="${p.id}" tabindex="0" aria-label="打开 ${p.id}. ${escapeHtml(p.title)}">
        <span class="problem-number">${String(p.order).padStart(2, '0')}</span>
        <div class="problem-main">
          <h3 class="problem-title">${p.id}. ${escapeHtml(p.title)}</h3>
          <div class="problem-meta"><span class="difficulty ${difficultyClass(p.difficulty)}">${difficultyLabel(p.difficulty)}</span><span>${escapeHtml(p.category)}</span><span>${escapeHtml(p.pattern)}</span></div>
        </div>
        <div class="card-actions">
          <button class="favorite-button ${isFavorite(p.id) ? 'active' : ''}" data-favorite="${p.id}" type="button" aria-label="${isFavorite(p.id) ? '取消收藏' : '收藏'}">${isFavorite(p.id) ? '★' : '☆'}</button>
          <button class="check-button ${isDone(p.id) ? 'active' : ''}" data-done="${p.id}" type="button" aria-label="${isDone(p.id) ? '标记未完成' : '标记已掌握'}">${isDone(p.id) ? '✓' : ''}</button>
        </div>
      </article>`).join('');
    renderActiveFilters();
  }
  function renderActiveFilters() {
    const chips = [];
    if (state.query) chips.push(`搜索：${escapeHtml(state.query)}`);
    if (state.status !== 'all') chips.push({todo:'未完成',done:'已掌握',favorite:'收藏'}[state.status]);
    if (state.difficulty !== 'ALL') chips.push(difficultyLabel(state.difficulty));
    if (state.category !== '全部专题') chips.push(state.category);
    els.activeFilters.innerHTML = chips.map(x => `<span class="filter-chip">${x}</span>`).join('');
  }
  function updateProgress() {
    const n = state.saved.done.length;
    els.doneCount.textContent = n;
    els.ring.style.setProperty('--progress', n);
    els.lineFill.style.width = `${n}%`;
    els.caption.textContent = n === 100 ? '全线通关。下一轮：闭卷复现。' : n >= 75 ? '最后冲刺，把薄弱题再做一遍。' : n >= 40 ? '已经越过最难的起步阶段。' : n ? '保持节奏，理解比速度更重要。' : '今天，从一道题开始。';
    const recent = problems.find(p => String(p.id) === String(state.saved.recent));
    els.continueBtn.textContent = recent ? `继续：${recent.id}. ${recent.title}` : '从第一题开始';
  }
  function renderMath(root) {
    if (!window.katex) return;
    root.querySelectorAll('[data-formula]').forEach(el => {
      try { window.katex.render(el.dataset.formula, el, { throwOnError: false, displayMode: true }); } catch (_) {}
    });
  }
  function openProblem(id) {
    const p = problems.find(x => String(x.id) === String(id)); if (!p) return;
    state.currentId = String(p.id); state.saved.recent = String(p.id); persist(); updateProgress();
    document.title = `${p.id}. ${p.title} · HOT 100`;
    els.favorite.textContent = isFavorite(p.id) ? '★' : '☆';
    els.favorite.classList.toggle('active', isFavorite(p.id));
    els.markDone.textContent = isDone(p.id) ? '✓ 已掌握（点击撤销）' : '标记为已掌握';
    const idx = problems.indexOf(p); els.prev.disabled = idx === 0; els.next.disabled = idx === problems.length - 1;
    els.detail.innerHTML = `
      <header class="detail-heading">
        <p class="eyebrow">第 ${p.order} / 100 题 · ${escapeHtml(p.category)}</p>
        <h2>${p.id}. ${escapeHtml(p.title)}</h2>
        <p>${escapeHtml(p.summary)}</p>
        <div class="detail-meta"><span class="tag difficulty ${difficultyClass(p.difficulty)}">${difficultyLabel(p.difficulty)}</span>${p.tags.map(t=>`<span class="tag">${escapeHtml(t)}</span>`).join('')}</div>
      </header>
      <section class="detail-section"><h3>破题信号</h3><div class="signal-card">${escapeHtml(p.signal)}</div></section>
      <section class="detail-section"><h3>核心不变量</h3><p>${escapeHtml(p.invariant)}</p></section>
      <details open><summary>分步推导</summary><div class="details-body"><ol class="steps">${p.steps.map(s=>`<li><span>${escapeHtml(s)}</span></li>`).join('')}</ol></div></details>
      <details><summary>公式与复杂度</summary><div class="details-body">
        ${p.formula ? `<div class="formula-card"><div data-formula="${escapeHtml(p.formula)}">${escapeHtml(p.formula)}</div></div>` : ''}
        <div class="complexity-grid"><div><small>时间复杂度</small><strong>${escapeHtml(p.time)}</strong></div><div><small>空间复杂度</small><strong>${escapeHtml(p.space)}</strong></div></div>
      </div></details>
      <section class="detail-section"><h3>高频易错</h3><div class="pitfall-card">${escapeHtml(p.pitfall)}</div></section>
      <details><summary>Python 3 参考实现</summary><div class="details-body"><div class="code-wrap"><button class="copy-button" type="button">复制代码</button><pre><code>${highlightPython(p.code)}</code></pre></div></div></details>
      <section class="detail-section"><a class="leetcode-link" href="https://leetcode.cn/problems/${encodeURIComponent(p.slug)}/" target="_blank" rel="noopener noreferrer">在力扣打开原题 ↗</a></section>`;
    if (!els.dialog.open) els.dialog.showModal();
    els.dialog.scrollTop = 0; renderMath(els.detail); location.hash = `problem-${p.id}`;
  }
  function closeDialog() {
    els.dialog.close(); state.currentId = null; document.title = 'LeetCode HOT 100 · 算法通关手册';
    if (location.hash.startsWith('#problem-')) history.replaceState(null, '', location.pathname + location.search);
  }
  function moveProblem(delta) {
    const idx = problems.findIndex(p => String(p.id) === state.currentId);
    if (idx >= 0 && problems[idx + delta]) openProblem(problems[idx + delta].id);
  }
  let toastTimer;
  function toast(msg) { els.toast.textContent = msg; els.toast.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(()=>els.toast.classList.remove('show'), 1800); }
  function resetFilters() {
    state.query=''; state.status='all'; state.difficulty='ALL'; state.category='全部专题'; els.search.value='';
    document.querySelectorAll('[data-status]').forEach(b=>b.classList.toggle('active', b.dataset.status==='all'));
    document.querySelectorAll('[data-difficulty]').forEach(b=>b.classList.toggle('active', b.dataset.difficulty==='ALL'));
    renderCategoryNav(); renderList();
  }
  function applyTheme(theme) { state.saved.theme = theme; document.documentElement.dataset.theme = theme; persist(); }

  els.list.addEventListener('click', e => {
    const done = e.target.closest('[data-done]'); if (done) { e.stopPropagation(); toggleIn(state.saved.done, done.dataset.done); toast(isDone(done.dataset.done)?'已标记掌握':'已撤销完成'); return; }
    const fav = e.target.closest('[data-favorite]'); if (fav) { e.stopPropagation(); toggleIn(state.saved.favorites, fav.dataset.favorite); toast(isFavorite(fav.dataset.favorite)?'已收藏':'已取消收藏'); return; }
    const card = e.target.closest('.problem-card'); if (card) openProblem(card.dataset.id);
  });
  els.list.addEventListener('keydown', e => { if ((e.key==='Enter'||e.key===' ') && e.target.matches('.problem-card')) { e.preventDefault(); openProblem(e.target.dataset.id); } });
  els.search.addEventListener('input', e => { state.query=e.target.value.trim(); renderList(); });
  $('#status-filters').addEventListener('click', e => { const b=e.target.closest('button'); if(!b)return; state.status=b.dataset.status; e.currentTarget.querySelectorAll('button').forEach(x=>x.classList.toggle('active',x===b)); renderList(); });
  $('#difficulty-filters').addEventListener('click', e => { const b=e.target.closest('button'); if(!b)return; state.difficulty=b.dataset.difficulty; e.currentTarget.querySelectorAll('button').forEach(x=>x.classList.toggle('active',x===b)); renderList(); });
  els.categoryNav.addEventListener('click', e => { const b=e.target.closest('button'); if(!b)return; state.category=b.dataset.category; renderCategoryNav(); renderList(); });
  $('#clear-filters').addEventListener('click', resetFilters);
  $('#dialog-close').addEventListener('click', closeDialog); $('#dialog-back').addEventListener('click', closeDialog);
  els.dialog.addEventListener('cancel', e => { e.preventDefault(); closeDialog(); });
  els.prev.addEventListener('click', ()=>moveProblem(-1)); els.next.addEventListener('click', ()=>moveProblem(1));
  els.markDone.addEventListener('click', () => { const on=toggleIn(state.saved.done,state.currentId); els.markDone.textContent=on?'✓ 已掌握（点击撤销）':'标记为已掌握'; toast(on?'进度已保存':'已撤销完成'); });
  els.favorite.addEventListener('click', () => { const on=toggleIn(state.saved.favorites,state.currentId); els.favorite.textContent=on?'★':'☆'; els.favorite.classList.toggle('active',on); toast(on?'已收藏':'已取消收藏'); });
  els.detail.addEventListener('click', async e => { const b=e.target.closest('.copy-button'); if(!b)return; const code=problems.find(p=>String(p.id)===state.currentId).code; try{await navigator.clipboard.writeText(code);b.textContent='已复制';setTimeout(()=>b.textContent='复制代码',1400);}catch(_){toast('复制失败，请手动选择代码');} });
  $('#random-button').addEventListener('click',()=>openProblem(problems[Math.floor(Math.random()*problems.length)].id));
  els.continueBtn.addEventListener('click',()=>openProblem(state.saved.recent || problems.find(p=>!isDone(p.id))?.id || problems[0].id));
  $('#study-mode-button').addEventListener('click',e=>{state.studyMode=!state.studyMode;document.body.classList.toggle('study-mode',state.studyMode);e.target.textContent=state.studyMode?'退出专注模式':'开启专注模式';window.scrollTo({top:0,behavior:'smooth'});});
  $('#theme-button').addEventListener('click',()=>applyTheme(state.saved.theme==='dark'?'light':'dark'));
  $('#export-button').addEventListener('click',()=>{ const blob=new Blob([JSON.stringify({exportedAt:new Date().toISOString(),...state.saved},null,2)],{type:'application/json'}); const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='leetcode-hot100-progress.json';a.click();URL.revokeObjectURL(a.href);toast('学习记录已导出'); });
  $('#reset-button').addEventListener('click',()=>{if(confirm('确定清空全部完成状态、收藏和最近阅读吗？')){state.saved={done:[],favorites:[],recent:null,theme:state.saved.theme};persist();updateProgress();renderList();toast('进度已重置');}});
  document.addEventListener('keydown', e => {
    if (e.key==='/' && document.activeElement!==els.search && !els.dialog.open) { e.preventDefault(); els.search.focus(); }
    if ((e.key==='r'||e.key==='R') && document.activeElement?.tagName!=='INPUT' && !els.dialog.open) openProblem(problems[Math.floor(Math.random()*problems.length)].id);
    if (els.dialog.open && e.key==='ArrowLeft') moveProblem(-1);
    if (els.dialog.open && e.key==='ArrowRight') moveProblem(1);
  });

  applyTheme(state.saved.theme || (matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'));
  renderCategoryNav(); renderList(); updateProgress();
  const hashMatch=location.hash.match(/^#problem-(.+)$/); if(hashMatch) openProblem(hashMatch[1]);
})();

