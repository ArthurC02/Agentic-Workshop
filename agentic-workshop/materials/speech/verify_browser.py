"""Headless Edge smoke checks for the generated Greenfield deck."""
from pathlib import Path
import json
import re
import subprocess
import html

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
WORK = REPO / '.codex-tmp/speech-browser'
WORK.mkdir(parents=True, exist_ok=True)
probe = r"""
<script>
setTimeout(async () => {
  const result = {slides: [], errors: [], actions: {}};
  try {
    for(let i=0;i<slides.length;i++) {
      index=i; render(); await new Promise(r=>setTimeout(r,30));
      const c=el('content'), st=el('stage');
      result.slides.push({id:slides[i].id, contentOverflow:c.scrollHeight-c.clientHeight,
        horizontalOverflow:c.scrollWidth-c.clientWidth,
        stageOverflow:st.scrollHeight-st.clientHeight, promptVisible:!el('prompt-box').hidden});
    }
    index=4;render();let clipboardValue='';
    Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{clipboardValue=value;}}});
    await copyPrompt();result.actions.copy=clipboardValue===slides[index].prompt;
    Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('blocked');}}});
    await copyPrompt();result.actions.copyFallback=el('status').textContent.length>0;
    if(document.activeElement)document.activeElement.blur();
    const k=(key)=>dispatchEvent(new KeyboardEvent('keydown',{key}));
    k('ArrowRight'); result.actions.next = index===5;
    k('ArrowLeft'); result.actions.prev = index===4;
    k('n'); result.actions.notes = !el('notes').hidden;
    k('Escape');result.actions.notesClosed=el('notes').hidden;
    k('o');result.actions.overview=overview.open;
    el('overview-list').children[2].click(); result.actions.jump=index===2&&!overview.open;
    toggleTimer();await new Promise(r=>setTimeout(r,1100));toggleTimer();updateTimer();
    result.actions.timer=elapsed()>=1000&&!running;
    el('reset').click();result.actions.reset=elapsed()===0;
    result.actions.assets = SPEECH_DATA.idea.includes('FARE-001') && SPEECH_DATA.feature.includes('Scenario Outline:') && SPEECH_DATA.handout.includes('人工確認') && !SPEECH_DATA.handout.includes('講者備註');
    const downloads=[];const blobs=new Map();let sequence=0;
    URL.createObjectURL=blob=>{const url='blob:probe-'+(++sequence);blobs.set(url,blob);return url;};
    HTMLAnchorElement.prototype.click=function(){downloads.push({name:this.download,url:this.href});};
    el('download-idea').click();el('download-feature').click();el('download-handout').click();
    result.actions.downloadPayload=downloads.length===3 && downloads[0].name==='idea.md' && await blobs.get(downloads[0].url).text()===SPEECH_DATA.idea && downloads[1].name==='booking.feature' && await blobs.get(downloads[1].url).text()===SPEECH_DATA.feature && downloads[2].name==='greenfield-handout.md' && await blobs.get(downloads[2].url).text()===SPEECH_DATA.handout;
    index=14;render();await new Promise(r=>setTimeout(r,30));
  } catch(e) {result.errors.push(String(e));}
  const report=document.createElement('pre');report.id='browser-report';report.hidden=true;report.textContent=JSON.stringify(result);document.body.append(report);
},100);
</script>
"""
source = (ROOT / '01-greenfield/greenfield-deck.html').read_text(encoding='utf-8')
target = WORK / 'probe.html'
target.write_text(source.replace('</body>', probe + '</body>'), encoding='utf-8')
# Edge headless on Windows writes nothing to stdout for --dump-dom; prefer Chrome.
browser = next(p for p in (Path('C:/Program Files/Google/Chrome/Application/chrome.exe'),
                           Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')) if p.exists())
command = [str(browser), '--headless', '--disable-gpu', '--no-first-run',
           '--no-default-browser-check', '--disable-background-networking',
           '--allow-file-access-from-files', '--window-size=1600,1000',
           '--virtual-time-budget=6000', '--dump-dom',
           '--user-data-dir=' + str(WORK / 'profile'),
           '--screenshot=' + str(WORK / 'architecture.png'), target.as_uri()]
run = subprocess.run(command, capture_output=True, text=True, encoding='utf-8',
                     errors='replace', timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
match = re.search(r'<pre id="browser-report"[^>]*>(.*?)</pre>', run.stdout, re.S)
(WORK / 'dom.html').write_text(run.stdout, encoding='utf-8')
if not match:
    print(run.stderr[-2500:])
    raise RuntimeError('Browser did not produce a probe report')
report = json.loads(html.unescape(match.group(1)))
(WORK / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
if report['errors'] or not all(value for key,value in report['actions'].items()):
    raise RuntimeError('Browser smoke check failed')
if any(s['stageOverflow']>1 or s['horizontalOverflow']>1 or s['contentOverflow']>1 for s in report['slides']):
    raise RuntimeError('Slide overflow')
