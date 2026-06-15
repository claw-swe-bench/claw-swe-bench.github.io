#!/usr/bin/env python3
"""
Render data/leaderboard.json into a single self-contained index.html.
Mirrors the SWE-bench leaderboard pattern (build.py -> static site), styled to
match opensquilla.ai exactly: dark "space" theme, orange brand (#f07010),
Space Grotesk / Inter / JetBrains Mono, starfield + nebula background, with a
dark/light theme toggle (dark default). Data is baked inline so index.html
opens by double-click (no server).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "leaderboard.json")
OUT = os.path.join(HERE, "index.html")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Claw-SWE-Bench Leaderboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<script>document.documentElement.setAttribute('data-theme', localStorage.getItem('theme')||'dark');</script>
<style>
:root{
  --brand:#f07010; --brand-light:#f59030; --brand-dark:#d06010;
  --surface:#0a0a0f; --card:#12121a; --hover:#1a1a26; --border:#2a2a3a;
  --t1:#f0f0f5; --t2:#9a9ab0; --t3:#6a6a80;
  --green:#22c55e; --blue:#3b82f6; --purple:#a855f7; --red:#ef4444;
  --font-sans:"Inter","Noto Sans SC",system-ui,-apple-system,sans-serif;
  --font-display:"Space Grotesk","Inter",system-ui,sans-serif;
  --font-mono:"JetBrains Mono",ui-monospace,monospace;
}
[data-theme="light"]{
  --surface:#f8f8fc; --card:#ffffff; --hover:#f0f0f5; --border:#e0e0ea;
  --t1:#1a1a2e; --t2:#4a4a60; --t3:#8a8aa0;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--surface);color:var(--t1);font-family:var(--font-sans);
  line-height:1.55;-webkit-font-smoothing:antialiased;font-feature-settings:"ss01","cv01","cv11"}
h1,h2,h3{font-family:var(--font-display);letter-spacing:-.025em}
a{color:var(--brand);text-decoration:none}
a:hover{color:var(--brand-light)}
.wrap{max-width:1152px;margin:0 auto;padding:0 24px}
.z{position:relative;z-index:10}

/* ---- space background ---- */
#sf{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:0}
[data-theme="light"] #sf{opacity:.08}
.nebula{position:fixed;inset:0;pointer-events:none;z-index:0;background:
  radial-gradient(ellipse 120% 60% at 70% 12%, rgba(240,112,16,.10), transparent 70%),
  radial-gradient(ellipse 80% 40% at 25% 55%, rgba(56,100,220,.05), transparent 60%),
  radial-gradient(ellipse 100% 50% at 50% 85%, rgba(168,85,247,.04), transparent 55%)}
[data-theme="light"] .nebula{opacity:0}

/* ---- nav ---- */
header.nav{position:fixed;top:0;left:0;right:0;z-index:50;
  border-bottom:1px solid var(--border);background:color-mix(in srgb,var(--surface) 90%,transparent);
  backdrop-filter:saturate(150%) blur(10px)}
.nav-in{display:flex;align-items:center;gap:24px;height:64px}
.brand{display:flex;align-items:center;gap:9px;font-size:18px;font-weight:700;color:var(--t1);font-family:var(--font-display)}
.brand:hover{color:var(--t1)}
.logo{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,var(--brand),#fbbf24);
  display:grid;place-items:center;color:#fff;font-size:16px;font-weight:800;box-shadow:0 0 18px rgba(240,112,16,.4)}
.brand .b{color:var(--brand)}
.nav .spacer{flex:1}
.nav a.link{color:var(--t2);font-size:14px;font-weight:500;transition:color .15s}
.nav a.link:hover{color:var(--t1)}
.gh{display:inline-flex;align-items:center;gap:6px}
.iconbtn{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;color:var(--t2);
  background:transparent;border:0;cursor:pointer;transition:.15s}
.iconbtn:hover{color:var(--t1);background:var(--hover)}
.btn{display:inline-flex;align-items:center;gap:8px;padding:9px 16px;border-radius:11px;
  font-size:14px;font-weight:600;border:1px solid var(--border);background:transparent;color:var(--t1);cursor:pointer;transition:.15s}
.btn:hover{background:var(--hover);color:var(--t1)}
.btn.primary{background:var(--brand);border-color:var(--brand);color:#fff;box-shadow:0 6px 24px rgba(240,112,16,.22)}
.btn.primary:hover{background:var(--brand-dark);color:#fff}

/* ---- hero (compact, left-aligned) ---- */
.glow{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse 560px 320px at 18% 0%, rgba(240,112,16,.15), transparent 70%)}
.hero{position:relative;padding:104px 0 40px;overflow:hidden}
.hero-inner{max-width:780px}
.hero-eyebrow{margin-bottom:14px}
.hero h1{font-size:44px;line-height:1.08;letter-spacing:-.03em;margin:0 0 14px;font-weight:700}
.hero h1 .accent{color:var(--brand)}
.hero p.lead{max-width:640px;margin:0;color:var(--t2);font-size:16.5px}
.cta{display:flex;gap:12px;justify-content:flex-start;margin:22px 0 0;flex-wrap:wrap}
.cta .btn{padding:11px 22px;border-radius:12px;font-size:14.5px}

/* ---- sections ---- */
section.board{padding:64px 0 0;border-top:1px solid var(--border);margin-top:64px}
section.board:first-of-type{border-top:0;margin-top:24px}
.sec-head{display:flex;align-items:flex-end;justify-content:space-between;gap:18px;flex-wrap:wrap;margin-bottom:20px}
.sec-head h2{font-size:30px;margin:6px 0 6px;font-weight:700}
.sec-head .sub{color:var(--t2);font-size:15px;margin:0;max-width:720px}
.tech-label{font-family:var(--font-mono);font-weight:500;letter-spacing:.06em;text-transform:uppercase;
  font-size:11.5px;color:var(--brand)}
.controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.seg{display:inline-flex;border:1px solid var(--border);border-radius:11px;overflow:hidden;background:var(--card)}
.seg button{border:0;background:transparent;color:var(--t2);font-size:13px;font-weight:600;padding:8px 14px;cursor:pointer;transition:.15s}
.seg button:hover{color:var(--t1)}
.seg button.on{background:var(--brand);color:#fff}
.toggle{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:var(--t2);cursor:pointer;
  border:1px solid var(--border);border-radius:11px;padding:8px 14px;background:var(--card)}
.toggle input{accent-color:var(--brand)}

/* ---- table ---- */
.card{background:transparent;border:1px solid var(--border);border-radius:18px;overflow:hidden}
.tbl-scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px}
thead th{background:var(--card);text-align:right;font-weight:500;color:var(--t3);
  font-size:12px;letter-spacing:.02em;padding:14px 16px;white-space:nowrap}
thead th.l{text-align:left}
thead th.sortable{cursor:pointer;user-select:none;transition:color .15s}
thead th.sortable:hover{color:var(--t1)}
thead th[data-k="total_pass1"]{color:var(--brand);font-weight:700}
thead th .arr{opacity:.45;font-size:10px;margin-left:4px}
thead th.act{color:var(--t1)}
thead th.act[data-k="total_pass1"]{color:var(--brand)}
thead th.act .arr{opacity:1}
tbody td{padding:13px 16px;border-top:1px solid color-mix(in srgb,var(--border) 55%,transparent);
  text-align:right;white-space:nowrap;vertical-align:middle}
tbody tr:nth-child(even){background:color-mix(in srgb,var(--card) 35%,transparent)}
tbody tr:hover{background:var(--hover)}
td.l{text-align:left}
.rank{color:var(--t3);font-variant-numeric:tabular-nums;width:34px;font-family:var(--font-mono);font-size:13px}
.rank.top{color:var(--brand);font-weight:700}
.sys{font-weight:600;color:var(--t1)}
td.org-col{color:var(--t2);font-size:13px}
td .tag{margin-left:0}
.tag{display:inline-block;font-size:10.5px;font-weight:600;padding:2px 7px;border-radius:6px;margin-left:8px;vertical-align:1px;
  font-family:var(--font-mono);letter-spacing:.02em}
.tag.open{color:var(--green);background:color-mix(in srgb,var(--green) 14%,transparent);border:1px solid color-mix(in srgb,var(--green) 35%,transparent)}
.tag.prop{color:var(--t2);background:var(--hover);border:1px solid var(--border)}
.tag.rt{color:var(--blue);background:color-mix(in srgb,var(--blue) 12%,transparent);border:1px solid color-mix(in srgb,var(--blue) 30%,transparent);margin-left:8px}
.score{position:relative;font-variant-numeric:tabular-nums;font-weight:700;min-width:104px;font-family:var(--font-display);color:var(--t1)}
.score .bar{position:absolute;left:16px;right:16px;bottom:6px;height:4px;border-radius:3px;background:color-mix(in srgb,var(--border) 70%,transparent)}
.score .bar i{display:block;height:100%;border-radius:3px;background:linear-gradient(90deg,var(--brand),var(--brand-light))}
.score b{position:relative;font-size:15px}
.num{font-variant-numeric:tabular-nums;font-family:var(--font-mono);font-size:13px}
.dim{color:var(--t3)}
.grp-title{font-size:13px;font-weight:600;color:var(--t1);padding:15px 16px 8px;background:var(--card)}
.grp-title .k{color:var(--t3);font-weight:400}
.divider{height:1px;background:var(--border)}

/* ---- footer ---- */
footer{margin-top:72px;border-top:1px solid var(--border);background:color-mix(in srgb,var(--card) 50%,transparent)}
.foot-in{padding:44px 0 64px;display:grid;grid-template-columns:1.3fr 1fr;gap:40px}
.foot h4{font-family:var(--font-mono);font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--brand);margin:0 0 12px}
.foot p,.foot li{font-size:14px;color:var(--t2)}
.foot code{font-family:var(--font-mono);font-size:.85em;background:var(--card);border:1px solid var(--border);padding:.1em .4em;border-radius:5px;color:var(--brand-light)}
.defs dt{font-weight:600;color:var(--t1);font-size:14px;margin-top:10px}
.defs dd{margin:0 0 2px;color:var(--t2);font-size:13px}
.note{font-size:13px;color:var(--t3);margin:12px 0 0}

@media(max-width:820px){
  .hero{padding:92px 0 30px}
  .hero h1{font-size:32px}
  .foot-in{grid-template-columns:1fr}
  .nav a.link{display:none}
}
</style>
</head>
<body>
<canvas id="sf"></canvas>
<div class="nebula"></div>

<header class="nav"><div class="wrap nav-in">
  <a class="brand" href="#top">Claw-SWE-Bench</a>
  <a class="link" href="#openclaw">OpenClaw × Models</a>
  <a class="link" href="#claws">Model × Claws</a>
  <span class="spacer"></span>
  <a class="link" href="#about">About</a>
  <a class="link gh" id="paperBtn" href="#" target="_blank" rel="noopener">Paper</a>
  <a class="link gh" id="ghBtn" href="#" target="_blank" rel="noopener">
    <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
    GitHub</a>
  <button class="iconbtn" id="themeToggle" aria-label="Toggle theme">
    <svg class="ic-dark" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
    <svg class="ic-light" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="display:none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
  </button>
</div></header>

<a id="top"></a>
<main class="wrap z">
  <section class="hero">
    <div class="glow"></div>
    <div class="z hero-inner">
      <div class="tech-label hero-eyebrow">Agent-harness benchmark · 350 tasks · 8 languages</div>
      <h1>Claw-SWE-Bench <span class="accent">Leaderboard</span></h1>
      <p class="lead" id="heroLead"></p>
      <div class="cta">
        <a class="btn primary" href="#openclaw">View leaderboard
          <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg></a>
        <a class="btn" id="paperBtn2" href="#" target="_blank" rel="noopener">Read the paper</a>
      </div>
    </div>
  </section>

  <section class="board" id="openclaw"></section>
  <section class="board" id="claws"></section>
</main>

<footer id="about"><div class="wrap foot-in">
  <div>
    <h4>About</h4>
    <p id="aboutText"></p>
    <p class="note"><b>OpenClaw × Models</b> fixes the harness and varies the LLM; <b>Model × Claws</b> fixes the LLM and varies the harness. The candidate patch is read from the repository <code>git diff</code>, not parsed from the agent's reply, so heterogeneous harnesses are comparable.</p>
    <p class="note" id="caveat"></p>
  </div>
  <div class="defs">
    <h4>Metrics</h4>
    <dl>
      <dt>Total Pass@1</dt><dd>% of instances RESOLVED by the official SWE-bench evaluator (1 run/instance). Primary ranking metric.</dd>
      <dt>Per-language Pass@1</dt><dd>Pass@1 within each of the 8 languages (toggle "Per-language").</dd>
      <dt>Cost (USD)</dt><dd>Total US-dollar cost of the full 350-instance run, as reported in the paper.</dd>
      <dt>Dur (s)</dt><dd>Mean per-instance wall-clock time — the primary cross-harness resource measure.</dd>
    </dl>
  </div>
</div></footer>

<script id="data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const M = DATA.meta, S = DATA.sections;
const fmtCost = v => v==null ? '<span class="dim">—</span>' : '$'+(v>=100?Math.round(v).toLocaleString():v.toFixed(1));
const fmtDur = d => d==null ? '<span class="dim">—</span>' : Math.round(d)+'s';
const esc = s => String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

document.getElementById('heroLead').textContent = M.description;
document.getElementById('aboutText').textContent = M.description;
document.getElementById('caveat').innerHTML =
  'All numbers are taken verbatim from the paper (<a href="'+M.paper+'" target="_blank" rel="noopener">arXiv</a>, Tables 2 &amp; 3). Cost is total USD over the 350-instance run. Open-weights / org tags are best-effort and editable in <code>data/leaderboard.json</code>.';
for(const id of ['paperBtn','paperBtn2']) document.getElementById(id).href = M.paper;
if(M.github) document.getElementById('ghBtn').href = M.github;

const LANGS = M.languages;

function tableHTML(rows, state, tid, kind){
  const showLang = state.lang;
  const max = Math.max(...rows.map(r=>r.total_pass1));
  const idHead = kind==='claws' ? ['Claw','Org'] : ['Model','Org','License'];
  const cols = [
    {k:'rank', l:'#', cls:'l', noSort:true},
    ...idHead.map(l=>({k:'_id', l, cls:'l', noSort:true})),
    {k:'total_pass1', l:'Pass@1', cls:''},
    ...(showLang ? LANGS.map(L=>({k:'lang:'+L, l:L, cls:''})) : []),
    {k:'cost_usd', l:'Cost (USD)', cls:''},
    {k:'avg_duration_s', l:'Dur (s)', cls:''},
  ];
  const getv = (r,k)=> k.startsWith('lang:') ? (r.per_language[k.slice(5)] ?? -1) : r[k];
  let sorted = rows.slice();
  if(state.key){
    const k=state.key, dir=state.dir;
    sorted.sort((a,b)=>{ let x=getv(a,k), y=getv(b,k); return (x>y?1:x<y?-1:0)*dir; });
  }
  const thead = '<tr>'+cols.map(c=>{
    const act = state.key===c.k ? ' act' : '';
    const arr = c.noSort ? '' : `<span class="arr">${state.key===c.k?(state.dir>0?'▲':'▼'):'↕'}</span>`;
    const so = c.noSort ? '' : ' sortable';
    return `<th class="${c.cls}${so}${act}" data-k="${c.k}">${c.l}${arr}</th>`;
  }).join('')+'</tr>';
  const body = sorted.map((r,i)=>{
    const top = (i===0 && (!state.key || (state.key==='total_pass1' && state.dir<0))) ? ' top':'';
    const idCells = kind==='claws'
      ? `<td class="l"><span class="sys">${esc(r.system)}</span></td><td class="l org-col">${esc(r.org||'')}</td>`
      : `<td class="l"><span class="sys">${esc(r.system)}</span></td><td class="l org-col">${esc(r.org||'')}</td><td class="l"><span class="tag ${r.open_weights?'open':'prop'}">${r.open_weights?'Open':'Proprietary'}</span></td>`;
    const langCells = showLang ? LANGS.map(L=>{
      const v=r.per_language[L]; return `<td class="num">${v==null?'<span class=dim>—</span>':v.toFixed(1)}</td>`;
    }).join('') : '';
    const w = (r.total_pass1/max*100).toFixed(1);
    return `<tr>
      <td class="l rank${top}">${i+1}</td>
      ${idCells}
      <td class="score"><b>${r.total_pass1.toFixed(1)}</b><span class="bar"><i style="width:${w}%"></i></span></td>
      ${langCells}
      <td class="num dim">${fmtCost(r.cost_usd)}</td>
      <td class="num dim">${fmtDur(r.avg_duration_s)}</td>
    </tr>`;
  }).join('');
  return `<div class="tbl-scroll"><table data-tid="${tid}"><thead>${thead}</thead><tbody>${body}</tbody></table></div>`;
}

const STATE = {};
function ensure(tid){ if(!STATE[tid]) STATE[tid]={key:'total_pass1',dir:-1,lang:false}; return STATE[tid]; }

function applyFilter(rows, mode){
  if(mode==='open') return rows.filter(r=>r.open_weights);
  if(mode==='prop') return rows.filter(r=>!r.open_weights);
  return rows;
}

function renderOpenclaw(){
  const sec=S.openclaw, st=ensure('openclaw');
  const rows=applyFilter(sec.rows, st.filter||'all');
  document.getElementById('openclaw').innerHTML = `
    <div class="sec-head">
      <div>
        <div class="tech-label">${M.split} · fixed: ${sec.fixed}</div>
        <h2>${sec.title}</h2><p class="sub">${sec.subtitle}</p>
      </div>
      <div class="controls">
        <span class="seg" id="ocFilter">
          <button data-f="all" class="${(st.filter||'all')==='all'?'on':''}">All</button>
          <button data-f="open" class="${st.filter==='open'?'on':''}">Open</button>
          <button data-f="prop" class="${st.filter==='prop'?'on':''}">Proprietary</button>
        </span>
        <label class="toggle"><input type="checkbox" id="ocLang" ${st.lang?'checked':''}> Per-language</label>
      </div>
    </div>
    <div class="card">${tableHTML(rows, st, 'openclaw', 'openclaw')}</div>`;
}

function renderClaws(){
  const sec=S.claws;
  const groups = sec.groups.map((g,gi)=>{
    const tid='claws'+gi, st=ensure(tid);
    return `<div class="grp-title">Model: <b>${esc(g.model)}</b> <span class="k">· 5 claws, same model</span></div>
            ${tableHTML(g.rows, st, tid, 'claws')}`;
  }).join('<div class="divider"></div>');
  const anyLang = ensure('claws0').lang;
  document.getElementById('claws').innerHTML = `
    <div class="sec-head">
      <div>
        <div class="tech-label">${M.split} · fixed: ${sec.fixed}</div>
        <h2>${sec.title}</h2><p class="sub">${sec.subtitle}</p>
      </div>
      <div class="controls">
        <label class="toggle"><input type="checkbox" id="clLang" ${anyLang?'checked':''}> Per-language</label>
      </div>
    </div>
    <div class="card">${groups}</div>`;
}

document.addEventListener('click', e=>{
  const th = e.target.closest('th.sortable'); if(!th) return;
  const tid = th.closest('table').dataset.tid, st=ensure(tid), k=th.dataset.k;
  if(st.key===k) st.dir*=-1; else {st.key=k; st.dir=(k==='system')?1:-1;}
  rerender();
});
document.addEventListener('change', e=>{
  if(e.target.id==='ocLang'){ ensure('openclaw').lang=e.target.checked; }
  else if(e.target.id==='clLang'){ S.claws.groups.forEach((_,gi)=>ensure('claws'+gi).lang=e.target.checked); }
  else return;
  rerender();
});
document.addEventListener('click', e=>{
  const b=e.target.closest('#ocFilter button'); if(!b) return;
  ensure('openclaw').filter=b.dataset.f; rerender();
});

function rerender(){ renderOpenclaw(); renderClaws(); }
rerender();

/* ---- theme toggle ---- */
(function(){
  function sync(){
    var dark = (document.documentElement.getAttribute('data-theme')||'dark')==='dark';
    var d=document.querySelector('.ic-dark'), l=document.querySelector('.ic-light');
    if(d) d.style.display = dark?'block':'none';
    if(l) l.style.display = dark?'none':'block';
  }
  sync();
  var btn=document.getElementById('themeToggle');
  if(btn) btn.addEventListener('click', function(){
    var cur=document.documentElement.getAttribute('data-theme')||'dark';
    var nxt=cur==='dark'?'light':'dark';
    document.documentElement.setAttribute('data-theme', nxt);
    localStorage.setItem('theme', nxt); sync();
  });
})();

/* ---- starfield ---- */
(function(){
  var c=document.getElementById('sf'); if(!c) return;
  var x=c.getContext('2d'); if(!x) return;
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var w,h,dpr=Math.min(window.devicePixelRatio||1,2),stars=[];
  function rs(){
    w=innerWidth;h=innerHeight;c.width=w*dpr;c.height=h*dpr;c.style.width=w+'px';c.style.height=h+'px';
    x.setTransform(1,0,0,1,0,0);x.scale(dpr,dpr);
    var n=Math.floor(w*h/7000);stars=[];
    for(var i=0;i<n;i++) stars.push({x:Math.random()*w,y:Math.random()*h,r:Math.random()*1.2+0.25,a:Math.random()*6.28,s:Math.random()*0.012+0.003});
  }
  function draw(){
    x.clearRect(0,0,w,h);
    for(var i=0;i<stars.length;i++){var st=stars[i];st.a+=st.s;var o=0.25+Math.abs(Math.sin(st.a))*0.7;
      x.globalAlpha=o;x.fillStyle=i%9===0?'#f5b070':'#cfd2ff';x.beginPath();x.arc(st.x,st.y,st.r,0,6.2832);x.fill();}
    x.globalAlpha=1;requestAnimationFrame(draw);
  }
  addEventListener('resize',rs);rs();draw();
})();
</script>
</body>
</html>
"""


def main():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__DATA__", payload)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {OUT} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
