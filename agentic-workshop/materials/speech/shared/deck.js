'use strict';
const slides = SPEECH_DATA.slides;
const el = id => document.getElementById(id);
let index = 0, notesVisible = false, running = false, accumulated = 0, startedAt = 0;
const overview = el('overview');
function node(tag, value, cls) { const n = document.createElement(tag); if(value !== undefined) n.textContent = value; if(cls) n.className = cls; return n; }
function announce(message) { el('status').textContent = message; }
function resize() {
  const available = Math.max(100, innerHeight - document.querySelector('nav').offsetHeight - 18);
  const scale = Math.min(innerWidth / 1600, available / 900);
  const stage = el('stage'); stage.style.transform = `scale(${scale})`;
  stage.style.left = `${(innerWidth - 1600 * scale) / 2}px`; stage.style.top = `${(available - 900 * scale) / 2}px`;
}
function render() {
  const s = slides[index]; el('chapter').textContent = s.chapter; el('title').textContent = s.title; el('lead').textContent = s.lead;
  const content = el('content'); content.replaceChildren();
  if(s.flow) { const flow = node('div', undefined, 'flow'); s.flow.forEach((v,i)=>{ if(i)flow.append(node('b','→'));flow.append(node('span',v)); });content.append(flow); }
  if(s.code) content.append(node('pre', s.code));
  if(s.cards) { const cards = node('div',undefined,'cards');s.cards.forEach(([title,body])=>{ const card=node('article',undefined,'card');card.append(node('h2',title),node('p',body));cards.append(card); });content.append(cards); }
  el('prompt-box').hidden = !s.prompt; el('prompt').textContent = s.prompt || '';
  el('check').textContent = '人工確認｜' + s.check; el('notes').textContent = '講者備註 · ' + (index+1) + '\n\n' + s.notes;
  el('notes').hidden = !notesVisible; el('counter').textContent = `${index+1} / ${slides.length}`;
  el('prev').disabled = index === 0; el('next').disabled = index === slides.length-1;
  document.title = `Greenfield · ${s.title}`; location.replace('#'+s.id);
  announce(''); document.querySelectorAll('#overview-list button').forEach((b,i)=>b.setAttribute('aria-current',String(i===index)));
  requestAnimationFrame(resize);
}
function move(delta){index=Math.max(0,Math.min(slides.length-1,index+delta));render();}
function toggleNotes(){notesVisible=!notesVisible;el('notes-button').setAttribute('aria-pressed',String(notesVisible));el('notes').hidden=!notesVisible;}
function openOverview(){if(!overview.open)overview.showModal();}
function elapsed(){return accumulated+(running?performance.now()-startedAt:0);}
function toggleTimer(){if(running){accumulated=elapsed();running=false;}else{startedAt=performance.now();running=true;}el('timer-button').textContent=running?'暫停 T':'計時 T';}
function updateTimer(){const secs=Math.floor(elapsed()/1000);el('timer').textContent=`${String(Math.floor(secs/60)).padStart(2,'0')}:${String(secs%60).padStart(2,'0')} / 45:00`;el('timer').classList.toggle('over',secs>=2700);}
function save(filename, value){const url=URL.createObjectURL(new Blob([value],{type:'text/plain;charset=utf-8'}));const a=node('a');a.href=url;a.download=filename;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);announce('已下載 '+filename);}
async function copyPrompt(){const value=slides[index].prompt;if(!value)return;try{await navigator.clipboard.writeText(value);announce('指令已複製');}catch{const t=node('textarea');t.value=value;document.body.append(t);t.select();let copied=false;try{copied=document.execCommand('copy');}catch{}t.remove();if(copied)announce('指令已複製');else{const range=document.createRange();range.selectNodeContents(el('prompt'));const selection=getSelection();selection.removeAllRanges();selection.addRange(range);announce('請按 Ctrl+C／Cmd+C 複製已選取的指令');}}}
el('prev').onclick=()=>move(-1);el('next').onclick=()=>move(1);el('copy').onclick=copyPrompt;
el('notes-button').onclick=toggleNotes;el('overview-button').onclick=openOverview;el('close-overview').onclick=()=>overview.close();
el('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{announce('請使用瀏覽器的全螢幕功能');}};
el('timer-button').onclick=toggleTimer;el('reset').onclick=()=>{running=false;accumulated=0;el('timer-button').textContent='計時 T';updateTimer();};
el('download-idea').onclick=()=>save('idea.md',SPEECH_DATA.idea);el('download-feature').onclick=()=>save('booking.feature',SPEECH_DATA.feature);el('download-handout').onclick=()=>save('greenfield-handout.md',SPEECH_DATA.handout);
slides.forEach((s,i)=>{const b=node('button',`${i+1}. ${s.title}`);b.onclick=()=>{index=i;overview.close();render();};el('overview-list').append(b);});
function fromHash(){const target=slides.findIndex(s=>s.id===location.hash.slice(1));if(target>=0&&target!==index){index=target;render();}}
addEventListener('hashchange',fromHash);addEventListener('resize',resize);
addEventListener('keydown',e=>{if((e.target instanceof Element&&e.target.closest('button,textarea,input,select'))||e.ctrlKey||e.metaKey||e.altKey)return;if(overview.open)return;const key=e.key.toLowerCase();if(['arrowright','pagedown',' '].includes(key)){e.preventDefault();move(1);}else if(['arrowleft','pageup'].includes(key)){e.preventDefault();move(-1);}else if(key==='home'){index=0;render();}else if(key==='end'){index=slides.length-1;render();}else if(key==='n')toggleNotes();else if(key==='o')openOverview();else if(key==='t')toggleTimer();else if(key==='f')el('fullscreen').click();else if(key==='escape'&&notesVisible)toggleNotes();});
fromHash();render();setInterval(updateTimer,500);resize();
