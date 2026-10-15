/* Tema día / noche / LATAM · Instituto Luterano Latinoamericano · MIT */
(function(){
  var K='ill-tema', T=['noche','dia','latam'];
  var L={noche:'🌙 Noche',dia:'☀️ Día',latam:'🌎 LATAM'};
  var h=document.documentElement;
  var t=localStorage.getItem(K);
  if(T.indexOf(t)<0){t=(window.matchMedia&&matchMedia('(prefers-color-scheme: light)').matches)?'dia':'noche';}
  h.setAttribute('data-tema',t);
  var css='html[data-tema=dia]{--void:#f7f2e4;--card:rgba(255,253,246,.94);--gold:#8a6d12;--gold-hot:#7a5c00;--line:rgba(138,109,18,.28);--line-hot:rgba(122,92,0,.6);--ink:#1f1b12;--muted:#6b6455;--violet:#5b3fd1;--emerald:#0a7d4f;--cyan:#006c86;--red:#b3261e;color-scheme:light}'+
  'html[data-tema=latam]{--void:#2a0b19;--card:rgba(58,16,36,.93);--gold:#f4b400;--gold-hot:#ffd23f;--line:rgba(244,180,0,.3);--line-hot:rgba(255,210,63,.65);--ink:#fff3df;--muted:#e0b9a6;--violet:#2ec4b6;--emerald:#43c463;--cyan:#22b8e0;--red:#ff5a5f}'+
  'html[data-tema=latam] body{background:linear-gradient(90deg,#e63946 0 20%,#f4b400 20% 40%,#43c463 40% 60%,#22b8e0 60% 80%,#7b2ff7 80%) top/100% 5px no-repeat,radial-gradient(ellipse at 50% -10%,rgba(244,180,0,.16),transparent 45%),var(--void)!important}'+
  'html[data-tema=dia] body{background:var(--void)!important}'+
  '#tema-btn{position:fixed;right:14px;bottom:14px;z-index:9999;font:700 13px/1 ui-monospace,Menlo,monospace;padding:10px 14px;border-radius:999px;border:1px solid var(--line-hot,var(--gold));background:var(--card,var(--void));color:var(--ink);box-shadow:0 4px 18px rgba(0,0,0,.25);cursor:pointer}'+
  '@media print{#tema-btn{display:none}}';
  var s=document.createElement('style');s.textContent=css;document.head.appendChild(s);
  function btn(){
    var b=document.createElement('button');b.id='tema-btn';b.type='button';
    b.setAttribute('aria-label','Cambiar tema: día, noche o LATAM');
    b.textContent=L[t];
    b.onclick=function(){t=T[(T.indexOf(t)+1)%3];h.setAttribute('data-tema',t);localStorage.setItem(K,t);b.textContent=L[t];};
    document.body.appendChild(b);
  }
  if(document.body)btn();else document.addEventListener('DOMContentLoaded',btn);
})();
