/* 20-deck-features.js — per-segment timers, unlock panels, gates, 60s countdown,
   workshop clock, presenter window (P) with postMessage sync.
   Plain ES2018 IIFE. Consumes window.DK (10-deck-core.js). Works on file://. */
(function () {
  'use strict';

  var booted = false;

  /* ---------- small helpers ---------- */
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function pad2(n) { n = Math.floor(Math.abs(n)); return n < 10 ? '0' + n : String(n); }
  function fmt(sec) { sec = Math.max(0, Math.floor(sec)); return pad2(sec / 60) + ':' + pad2(sec % 60); }
  /* "mm:ss" -> seconds; "mm" -> minutes*60; "07–29" -> first number as minutes */
  function parseMMSS(s) {
    s = String(s || '').trim();
    var m = s.match(/^(\d+):(\d{1,2})/);
    if (m) return parseInt(m[1], 10) * 60 + parseInt(m[2], 10);
    m = s.match(/^(\d+)/);
    return m ? parseInt(m[1], 10) * 60 : NaN;
  }
  function now() { return Date.now(); }
  function codes() {
    var c = window.DECK_CODES;
    if (c && !Array.isArray(c) && Array.isArray(c.groups)) c = c.groups;
    return Array.isArray(c) ? c : [];
  }
  function codeFor(id) {
    var list = codes();
    for (var i = 0; i < list.length; i++) if (list[i] && list[i].id === id) return list[i];
    return null;
  }
  function insertBeforeNotes(slide, node) {
    var notes = null;
    for (var i = 0; i < slide.children.length; i++) {
      if (slide.children[i].classList.contains('notes')) { notes = slide.children[i]; break; }
    }
    if (notes) slide.insertBefore(node, notes); else slide.appendChild(node);
  }

  /* ---------- boot: wait for DOMContentLoaded and window.DK ---------- */
  function tryBoot(attempt) {
    if (booted) return;
    if (window.DK && window.DK.slides && window.DK.PLAN) {
      booted = true;
      try { init(window.DK); } catch (e) { if (window.console) console.error('[deck-features]', e); throw e; }
      return;
    }
    if ((attempt || 0) < 200) setTimeout(function () { tryBoot((attempt || 0) + 1); }, 25);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { tryBoot(0); });
  } else {
    setTimeout(function () { tryBoot(0); }, 0);
  }

  /* ======================================================================= */
  function init(DK) {
    var slides = Array.prototype.slice.call(DK.slides || []);
    var PLAN = DK.PLAN || [];
    var isPresenter = !!DK.isPresenter || location.hash.indexOf('#presenter') === 0;

    function segOf(i) { return typeof DK.segOf === 'function' ? DK.segOf(i) : (slides[i] && slides[i].getAttribute('data-seg')); }
    function planOf(seg) {
      for (var i = 0; i < PLAN.length; i++) if (PLAN[i].seg === seg) return PLAN[i];
      return null;
    }
    function segLabel(seg) { var p = planOf(seg); return p ? p.label : (seg || ''); }
    function curIndex() { var i = DK.index; return typeof i === 'number' && i >= 0 ? i : 0; }
    function curFrag() { var f = DK.frag; return typeof f === 'number' ? f : 0; }
    function curSlide() { return slides[curIndex()] || null; }
    function slideIndexOf(node) { return slides.indexOf(node); }

    /* ---------------- state ---------------- */
    var timers = {};          // seg -> {dur (s), elapsed (ms), running, startedAt (epoch ms)}
    var countdowns = {};      // slide index -> {total (s), startedAt, state}
    var workshopStart = null; // epoch ms

    PLAN.forEach(function (p) {
      var dur = (p.end - p.start) * 60;
      for (var i = 0; i < slides.length; i++) {
        var s = slides[i];
        if (s.hasAttribute('data-timer') && (s.getAttribute('data-seg') === p.seg || segOf(i) === p.seg)) {
          var d = parseMMSS(s.getAttribute('data-timer'));
          if (!isNaN(d) && d > 0) { dur = d; break; }
        }
      }
      timers[p.seg] = { dur: dur, elapsed: 0, running: false, startedAt: 0 };
    });

    function tmr(seg) {
      if (!seg) return null;
      if (!timers[seg]) {
        var p = planOf(seg);
        timers[seg] = { dur: p ? (p.end - p.start) * 60 : 600, elapsed: 0, running: false, startedAt: 0 };
      }
      return timers[seg];
    }
    function elapsedMs(t) { return t ? t.elapsed + (t.running ? Math.max(0, now() - t.startedAt) : 0) : 0; }
    function timerState(t) {
      if (!t) return 'idle';
      var e = elapsedMs(t) / 1000;
      if (!t.running && e <= 0) return 'idle';
      if (e > t.dur) return 'over';
      if (t.dur - e <= t.dur * 0.2) return 'warn';
      return t.running ? 'running' : 'paused';
    }
    function timerText(t) {
      if (!t) return '--:--';
      var rem = t.dur - elapsedMs(t) / 1000;
      if (rem >= 0) return fmt(Math.ceil(rem - 1e-6));
      return '+' + fmt(-rem);
    }
    function timerHint(t) {
      var st = timerState(t);
      if (st === 'idle') return '按 T 開始計時';
      if (st === 'over') return '已超時 · R 重設';
      if (!t.running) return '已暫停 · T 繼續 · R 重設';
      return 'T 暫停 · R 重設';
    }

    /* ---------------- timer commands ---------------- */
    function startTimer(seg) {
      var t = tmr(seg); if (!t || t.running) return;
      Object.keys(timers).forEach(function (k) {         // only one segment runs at a time
        var o = timers[k];
        if (k !== seg && o.running) { o.elapsed = elapsedMs(o); o.running = false; }
      });
      t.startedAt = now(); t.running = true;
      if (workshopStart == null && seg === 'opening') workshopStart = t.startedAt - t.elapsed;
    }
    function pauseTimer(seg) {
      var t = tmr(seg); if (!t || !t.running) return;
      t.elapsed = elapsedMs(t); t.running = false;
    }
    function resetTimer(seg) {
      var t = tmr(seg); if (!t) return;
      t.elapsed = 0; t.running = false; t.startedAt = 0;
    }
    function toggleTimer(seg) {
      var t = tmr(seg); if (!t) return;
      if (t.running) pauseTimer(seg); else startTimer(seg);
    }

    /* ---------------- countdown commands ---------------- */
    function cdOf(i) {
      var s = slides[i];
      if (!s || !s.hasAttribute('data-countdown')) return null;
      if (!countdowns[i]) {
        var total = parseInt(s.getAttribute('data-countdown'), 10);
        countdowns[i] = { total: total > 0 ? total : 60, elapsed: 0, startedAt: 0, state: 'idle' };
      }
      return countdowns[i];
    }
    function cdRemaining(c) {
      if (!c) return 0;
      if (c.state === 'idle') return c.total;
      if (c.state === 'done') return 0;
      return Math.max(0, c.total - ((c.elapsed || 0) + (c.state === 'running' ? Math.max(0, now() - c.startedAt) : 0)) / 1000);
    }
    function startCountdown(i) {
      var c = cdOf(i); if (!c) return;
      if (c.state === 'running' || c.state === 'done') return;
      c.startedAt = now(); c.state = 'running';
    }
    function pauseCountdown(i) {
      var c = cdOf(i); if (!c || c.state !== 'running') return;
      c.elapsed = Math.min(c.total * 1000, (c.elapsed || 0) + Math.max(0, now() - c.startedAt));
      c.startedAt = 0; c.state = c.elapsed >= c.total * 1000 ? 'done' : 'paused';
    }
    function resetCountdown(i) {
      var c = cdOf(i); if (!c) return;
      c.elapsed = 0; c.startedAt = 0; c.state = 'idle';
    }
    function toggleCountdown(i) {
      var c = cdOf(i); if (!c) return;
      if (c.state === 'running') pauseCountdown(i);
      else startCountdown(i);                         // idle/paused -> start/resume; R resets done
    }

    /* Single entry for T/R and remote commands; acts on the current slide/segment. */
    function command(cmd) {
      var i = curIndex(), s = slides[i], seg = segOf(i);
      var onCd = !!(s && s.hasAttribute('data-countdown'));
      if (cmd === 'toggle') { if (onCd) toggleCountdown(i); else toggleTimer(seg); }
      else if (cmd === 'reset') { if (onCd) resetCountdown(i); else resetTimer(seg); }
      else if (cmd === 'start') { if (onCd) startCountdown(i); else startTimer(seg); }
      else if (cmd === 'pause') { if (onCd) pauseCountdown(i); else pauseTimer(seg); }
      else if (cmd === 'reset-timer') { if (onCd) resetCountdown(i); else resetTimer(seg); }
      else if (cmd === 'workshop') workshopStart = now();
      renderAll();
      sendState(true);
    }

    /* ---------------- decorate slides ---------------- */
    var SVGNS = 'http://www.w3.org/2000/svg';
    var CIRC = 339.292; // 2 * PI * 54

    // Speaker-notes placeholders (e.g. on-demand Recovery codes): <code data-code="recovery-b1"></code>
    document.querySelectorAll('code[data-code]').forEach(function (c) {
      var g = codeFor(c.getAttribute('data-code'));
      c.textContent = g && g.code ? g.code : '（找不到解鎖碼：' + c.getAttribute('data-code') + '）';
    });

    slides.forEach(function (s, i) {
      var seg = s.getAttribute('data-seg') === 'reveal' ? segOf(i) : (s.getAttribute('data-seg') || segOf(i));

      if (s.hasAttribute('data-timer') && !$('.dk-timer-big', s)) {
        var big = el('div', 'dk-timer-big');
        big.setAttribute('data-seg', seg);
        big.setAttribute('data-state', 'idle');
        big.appendChild(el('div', 'dk-timer-time', timerText(tmr(seg))));
        big.appendChild(el('div', 'dk-timer-hint', timerHint(tmr(seg))));
        insertBeforeNotes(s, big);
      }

      if (s.hasAttribute('data-unlock') && !$('.dk-unlock', s)) {
        var id = s.getAttribute('data-unlock');
        var g = codeFor(id);
        var box = el('div', 'dk-unlock');
        box.setAttribute('data-unlock-id', id);
        box.appendChild(el('div', 'dk-unlock-label', '解鎖碼 · ' + (g && g.label ? g.label : segLabel(id))));
        var code = el('div', 'dk-unlock-code', g && g.code ? g.code : '（找不到解鎖碼：' + id + '）');
        if (!g || !g.code) code.setAttribute('data-missing', '');
        box.appendChild(code);
        box.appendChild(el('div', 'dk-unlock-help', '請在 Runbook 輸入此碼（不分大小寫，空白與連字號可省略）'));
        insertBeforeNotes(s, box);
      }

      if (s.hasAttribute('data-gates') && !$('.dk-gates-clock', s)) {
        var gseg = s.getAttribute('data-gates') || seg;
        var gc = el('div', 'dk-gates-clock');
        gc.setAttribute('data-seg', gseg);
        gc.setAttribute('data-state', 'idle');
        insertBeforeNotes(s, gc);
      }

      if (s.hasAttribute('data-countdown') && !$('.dk-countdown', s)) {
        var c = cdOf(i);
        var cd = el('div', 'dk-countdown');
        cd.setAttribute('data-cd', String(i));
        cd.setAttribute('data-state', 'idle');
        cd.setAttribute('role', 'button');
        cd.setAttribute('tabindex', '0');
        cd.setAttribute('title', '60 秒倒數：點擊或 T 開始／暫停／繼續；R 重設（段落計時持續）');
        cd.setAttribute('aria-label', '60 秒倒數：點擊或 T 開始／暫停／繼續；R 重設');
        var svg = document.createElementNS(SVGNS, 'svg');
        svg.setAttribute('viewBox', '0 0 120 120');
        svg.setAttribute('aria-hidden', 'true');
        svg.setAttribute('class', 'dk-ring');           // deck.css rotates .dk-ring by -90deg
        var track = document.createElementNS(SVGNS, 'circle');
        track.setAttribute('class', 'dk-ring-bg dk-count-track');
        var ring = document.createElementNS(SVGNS, 'circle');
        ring.setAttribute('class', 'dk-ring-fg dk-count-ring');
        [track, ring].forEach(function (cc) {
          cc.setAttribute('cx', '60'); cc.setAttribute('cy', '60'); cc.setAttribute('r', '54');
          cc.setAttribute('fill', 'none');
        });
        ring.setAttribute('stroke-dasharray', String(CIRC));
        ring.setAttribute('stroke-dashoffset', '0');
        svg.appendChild(track); svg.appendChild(ring);
        cd.appendChild(svg);
        cd.appendChild(el('div', 'dk-count-num', String(c ? c.total : 60)));
        insertBeforeNotes(s, cd);
      }
    });

    /* Fit-to-slide safety net: if a slide's flow content runs past the safe area (above the
       agenda bar), shrink its children uniformly with CSS zoom. ponytail: zoom floor 0.7 —
       a slide that needs more than that should be split, not shrunk (see console warning). */
    function fitSlide(s) {
      var kids = Array.prototype.filter.call(s.children, function (c) {
        if (c.tagName === 'ASIDE') return false;
        var pos = getComputedStyle(c).position;
        return pos !== 'absolute' && pos !== 'fixed';
      });
      kids.forEach(function (c) { c.style.zoom = ''; });
      var limit = s.clientHeight - parseFloat(getComputedStyle(s).paddingBottom);
      function bottom() {
        return kids.reduce(function (m, c) { return Math.max(m, c.getBoundingClientRect().bottom); }, 0);
      }
      var top = s.getBoundingClientRect().top, k = s.getBoundingClientRect().height / s.offsetHeight || 1;
      var z = 1;
      for (var n = 0; n < 12 && (bottom() - top) / k > limit + 1 && z > 0.7; n++) {
        z = Math.max(0.7, z - 0.03);
        kids.forEach(function (c) { c.style.zoom = String(z); });
      }
      if ((bottom() - top) / k > limit + 1 && window.console) {
        console.warn('[deck] slide still overflows after fit:', s.getAttribute('data-title'));
      }
    }
    function fitAll() { slides.forEach(fitSlide); }
    fitAll();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitAll);
    window.addEventListener('load', fitAll);

    /* Countdown click (capture + delegation; also covers presenter clones). */
    document.addEventListener('click', function (e) {
      var t = e.target && e.target.closest ? e.target.closest('.dk-countdown') : null;
      if (!t) return;
      var i = parseInt(t.getAttribute('data-cd'), 10);
      if (isNaN(i)) return;
      e.preventDefault();
      e.stopPropagation();
      if (isPresenter) { remote({ action: 'timer', cmd: 'countdown', index: i }); return; }
      toggleCountdown(i); renderAll(); sendState(true);
    }, true);

    /* ---------------- rendering (document-wide, so presenter clones update too) ---------------- */
    function setState(node, st) { if (node.getAttribute('data-state') !== st) node.setAttribute('data-state', st); }
    function setText(node, txt) { if (node && node.textContent !== txt) node.textContent = txt; }

    function renderTimers() {
      $$('.dk-timer-big').forEach(function (big) {
        var t = tmr(big.getAttribute('data-seg'));
        setState(big, timerState(t));
        setText($('.dk-timer-time', big), timerText(t));
        setText($('.dk-timer-hint', big), timerHint(t));
      });
      var chip = $('#dk-chrome .dk-timer-chip') || $('.dk-timer-chip');
      if (chip) {
        var seg = segOf(curIndex()), t = tmr(seg), st = timerState(t);
        var show = !!t && st !== 'idle';
        if (chip.hidden === show) chip.hidden = !show;
        if (show) {
          setState(chip, st);
          chip.setAttribute('data-seg', seg);
          var lab = $('.dk-chip-label', chip), tim = $('.dk-chip-time', chip);
          if (!lab || !tim) {
            chip.textContent = '';
            lab = chip.appendChild(el('span', 'dk-chip-label'));
            tim = chip.appendChild(el('span', 'dk-chip-time'));
          }
          setText(lab, segLabel(seg) + (t.running ? '' : ' · 暫停'));
          setText(tim, timerText(t));
        }
      }
    }

    function renderGates() {
      $$('section.slide[data-gates]').forEach(function (s) {
        var seg = s.getAttribute('data-gates') || s.getAttribute('data-seg');
        var t = tmr(seg), e = elapsedMs(t) / 1000, st = timerState(t), started = st !== 'idle';
        var lis = $$('.timeline > li', s);
        var mins = lis.map(function (li) { var m = $('.tl-min', li); return parseMMSS(m ? m.textContent : ''); });
        var cur = -1;
        if (started) {
          for (var k = 0; k < mins.length; k++) if (!isNaN(mins[k]) && mins[k] <= e) cur = k;
        }
        var over = started && !!t && e >= t.dur;
        lis.forEach(function (li, k) {
          li.classList.toggle('is-done', started && (over || k < cur));
          li.classList.toggle('is-current', started && !over && k === cur);
        });
        var gc = $('.dk-gates-clock', s);
        if (gc) {
          setState(gc, st);
          setText(gc, segLabel(seg) + ' ' + fmt(e) + ' / ' + fmt(t ? t.dur : 0));
        }
      });
    }

    function renderCountdowns() {
      $$('.dk-countdown').forEach(function (cd) {
        var i = parseInt(cd.getAttribute('data-cd'), 10);
        var c = cdOf(i); if (!c) return;
        if (c.state === 'running' && cdRemaining(c) <= 0) { c.elapsed = c.total * 1000; c.startedAt = 0; c.state = 'done'; }
        var rem = cdRemaining(c);
        setState(cd, c.state);
        setText($('.dk-count-num', cd), String(Math.ceil(rem - 1e-6)));
        var ring = $('.dk-count-ring', cd);
        if (ring) ring.setAttribute('stroke-dashoffset', (CIRC * (1 - rem / c.total)).toFixed(3));
      });
    }

    function renderAll() {
      renderTimers();
      renderGates();
      renderCountdowns();
      if (isPresenter) renderPresenterTick();
    }

    /* ---------------- postMessage sync ---------------- */
    var presenterWin = null;               // main side: presenter window
    var lastSent = 0;
    var remoteApplying = false;            // presenter side: applying main's state
    var gotState = false;                  // presenter side: received at least one state
    var lastRemote = { index: -1, frag: -1 };

    function post(win, msg) {
      try { if (win && !win.closed) { win.postMessage(msg, '*'); return true; } } catch (e) { /* ignore */ }
      return false;
    }
    function snapshot() {
      return { type: 'dk', action: 'state', index: curIndex(), frag: curFrag(),
        timers: timers, workshopStart: workshopStart, countdowns: countdowns };
    }
    function sendState(force) {
      if (isPresenter || !presenterWin || presenterWin.closed) return;
      var t = now();
      if (!force && t - lastSent < 1000) return;
      lastSent = t;
      post(presenterWin, snapshot());
    }
    /* presenter -> main; without an opener the presenter works standalone */
    function remote(msg) {
      msg.type = 'dk';
      var op = null;
      try { op = window.opener; } catch (e) { op = null; }
      if (op && !op.closed && post(op, msg)) return;
      if (msg.action === 'timer') {
        if (msg.cmd === 'countdown') { toggleCountdown(msg.index); renderAll(); }
        else command(msg.cmd);
      }
    }
    function applyState(d) {
      if (d.timers && typeof d.timers === 'object') timers = d.timers;
      if (d.countdowns && typeof d.countdowns === 'object') countdowns = d.countdowns;
      workshopStart = typeof d.workshopStart === 'number' ? d.workshopStart : null;
      gotState = true;
      var i = d.index | 0, f = d.frag | 0;
      lastRemote = { index: i, frag: f };
      if (i !== curIndex() || f !== curFrag()) {
        remoteApplying = true;
        try { DK.go(i, f); } finally { remoteApplying = false; }
      }
      if (pv && pv.shown !== curIndex() + ':' + curFrag()) renderPresenterFull();
      renderAll();
    }

    window.addEventListener('message', function (e) {
      var d = e.data;
      if (!d || typeof d !== 'object' || d.type !== 'dk') return;
      if (!isPresenter) {
        if (e.source && e.source !== window) presenterWin = e.source;
        if (d.action === 'hello') sendState(true);
        else if (d.action === 'go') {
          var i = d.index | 0, f = d.frag | 0;
          if (i !== curIndex() || f !== curFrag()) DK.go(i, f); else sendState(true);
        } else if (d.action === 'timer') {
          if (d.cmd === 'countdown') { toggleCountdown(d.index | 0); renderAll(); sendState(true); }
          else command(d.cmd);
        }
      } else if (d.action === 'state') {
        var op = null;
        try { op = window.opener; } catch (err) { op = null; }
        if (!op || e.source === op) applyState(d);
      }
    });

    function openPresenter() {
      if (presenterWin && !presenterWin.closed) { try { presenterWin.focus(); } catch (e) { /* ignore */ } sendState(true); return; }
      var url = location.href.split('#')[0] + '#presenter';
      presenterWin = window.open(url, 'dk-presenter', 'width=1400,height=850');
    }

    /* ---------------- presenter view (#pv-root) ---------------- */
    var pv = null;

    function btn(cls, text, attr, val) {
      var b = el('button', cls, text);
      b.type = 'button';
      if (attr) b.setAttribute(attr, val);
      return b;
    }
    function frameBox(cls) {               // panel label comes from deck.css ::before
      var box = el('div', cls);
      var frame = el('div', 'pv-frame');
      frame.style.position = 'relative';
      frame.style.overflow = 'hidden';
      frame.style.width = '100%';
      frame.style.aspectRatio = '16 / 9';
      box.appendChild(frame);
      return { box: box, frame: frame };
    }

    function buildPresenter() {
      document.body.classList.add('is-presenter');
      document.title = '主持人視窗 · ' + document.title;
      var root = el('div'); root.id = 'pv-root';
      var cur = frameBox('pv-current');
      var nxt = frameBox('pv-next');
      var nextTitle = nxt.box.appendChild(el('div', 'pv-next-title'));
      var notes = el('div', 'pv-notes');

      var timer = el('div', 'pv-timer');
      var tLabel = timer.appendChild(el('div', 'pv-timer-label'));
      var tTime = timer.appendChild(el('div', 'pv-timer-time'));
      var tBtns = timer.appendChild(el('div', 'pv-timer-btns'));
      tBtns.appendChild(btn('pv-btn', '開始', 'data-cmd', 'start'));
      tBtns.appendChild(btn('pv-btn', '暫停', 'data-cmd', 'pause'));
      tBtns.appendChild(btn('pv-btn', '重設', 'data-cmd', 'reset-timer'));

      var clock = el('div', 'pv-clock');
      var clockTime = clock.appendChild(el('span', 'pv-clock-time'));
      var wsBtn = clock.appendChild(btn('pv-btn pv-ws-start', '開始工作坊', 'data-cmd', 'workshop'));
      var plan = el('div', 'pv-plan');
      var planText = plan.appendChild(el('div', 'pv-plan-text'));
      var nowCodes = plan.appendChild(el('div', 'pv-now'));

      var codesBox = el('div', 'pv-codes');
      var table = codesBox.appendChild(el('table'));
      var thr = table.appendChild(el('thead')).appendChild(el('tr'));
      ['分鐘', '段落', '解鎖碼'].forEach(function (h) { thr.appendChild(el('th', null, h)); });
      var tbody = table.appendChild(el('tbody'));
      var rows = codes().map(function (g) {
        var tr = tbody.appendChild(el('tr'));
        tr.setAttribute('data-id', g.id);
        tr.appendChild(el('td', 'pv-code-min', pad2(g.minute)));
        tr.appendChild(el('td', 'pv-code-label', g.label || g.id));
        tr.appendChild(el('td', 'pv-code-code')).appendChild(el('code', null, g.code));
        return tr;
      });

      var controls = el('div', 'pv-controls');
      controls.appendChild(btn('pv-btn pv-prev', '◀', 'data-nav', 'prev'));
      var count = controls.appendChild(el('span', 'pv-count'));
      controls.appendChild(btn('pv-btn pv-next-btn', '▶', 'data-nav', 'next'));
      var link = controls.appendChild(el('span', 'pv-link', '連線中…'));

      [cur.box, nxt.box, notes, timer, clock, plan, codesBox, controls].forEach(function (n) { root.appendChild(n); });
      document.body.appendChild(root);

      root.addEventListener('click', function (e) {
        var b = e.target && e.target.closest ? e.target.closest('button') : null;
        if (!b) return;
        var cmd = b.getAttribute('data-cmd'), nav = b.getAttribute('data-nav');
        if (cmd) remote({ action: 'timer', cmd: cmd });
        else if (nav === 'prev') DK.prev();
        else if (nav === 'next') DK.next();
      });
      window.addEventListener('resize', fitFrames);

      pv = { root: root, curFrame: cur.frame, nextFrame: nxt.frame, nextTitle: nextTitle, notes: notes,
        timer: timer, tLabel: tLabel, tTime: tTime, clockTime: clockTime, wsBtn: wsBtn, plan: planText, now: nowCodes,
        rows: rows, count: count, link: link, shown: '' };
    }

    function cloneInto(frame, i, showAllFx) {
      frame.textContent = '';
      var s = slides[i];
      if (!s) { frame.appendChild(el('div', 'pv-empty', '（已是最後一頁）')); return; }
      var c = s.cloneNode(true);
      $$('.notes', c).forEach(function (n) { n.parentNode.removeChild(n); });
      c.removeAttribute('id');
      $$('[id]', c).forEach(function (n) { n.removeAttribute('id'); });
      c.classList.remove('is-past', 'is-future');
      c.classList.add('is-active', 'pv-clone');
      if (showAllFx) $$('.fx', c).forEach(function (f) { f.classList.add('is-shown'); });
      c.style.position = 'absolute'; c.style.left = '0'; c.style.top = '0';
      c.style.width = '1920px'; c.style.height = '1080px'; c.style.margin = '0';
      c.style.transform = 'none'; c.style.opacity = '1'; c.style.visibility = 'visible';
      var scaler = el('div', 'pv-scaler');
      scaler.style.cssText = 'position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;overflow:hidden;';
      scaler.appendChild(c);
      frame.appendChild(scaler);
    }
    function fitFrames() {
      if (!pv) return;
      [pv.curFrame, pv.nextFrame].forEach(function (f) {
        var sc = $('.pv-scaler', f), w = f.clientWidth;
        if (sc && w > 0) sc.style.transform = 'scale(' + (w / 1920).toFixed(5) + ')';
      });
    }

    function renderPresenterFull() {
      if (!pv) return;
      var i = curIndex(), s = slides[i];
      pv.shown = i + ':' + curFrag();
      cloneInto(pv.curFrame, i, false);
      cloneInto(pv.nextFrame, i + 1, true);
      var ns = slides[i + 1];
      var h = ns ? $('h1, h2', ns) : null;
      pv.nextTitle.textContent = ns ? (ns.getAttribute('data-title') || (h ? h.textContent.trim() : '')) : '—';
      var notes = s ? $('.notes', s) : null;
      pv.notes.innerHTML = notes && notes.innerHTML.trim() ? notes.innerHTML : '<p class="pv-no-notes">（本頁無備註）</p>';
      pv.count.textContent = (i + 1) + ' / ' + slides.length;
      var seg = segOf(i);
      // Codes released at this slide's minute (incl. on-demand Recovery codes) or for its segment.
      var sm = s && s.hasAttribute('data-minute') ? parseInt(s.getAttribute('data-minute'), 10) : NaN;
      var hits = codes().filter(function (g) { return g.id === seg || (!isNaN(sm) && g.minute === sm); });
      pv.rows.forEach(function (tr) {
        tr.classList.toggle('is-current', hits.some(function (g) { return g.id === tr.getAttribute('data-id'); }));
      });
      pv.now.textContent = '';
      if (hits.length) pv.now.appendChild(el('div', 'pv-now-title', '本時點解鎖碼'));
      hits.forEach(function (g) {
        var row = pv.now.appendChild(el('div', 'pv-now-row'));
        row.appendChild(el('span', 'pv-now-label', g.label || g.id));
        row.appendChild(el('code', null, g.code));
      });
      pv.now.hidden = !hits.length;
      fitFrames();
      setTimeout(fitFrames, 0);
    }

    function renderPresenterTick() {
      if (!pv) return;
      var i = curIndex(), seg = segOf(i), t = tmr(seg), st = timerState(t);
      var countdown = cdOf(i);
      if (countdown) {
        setText(pv.tLabel, fmt(countdown.total) + ' 倒數 · 按鈕僅控制本頁倒數；' + segLabel(seg) + ' 段落 ' + timerText(t) + (t && t.running ? '（持續計時）' : ''));
        setText(pv.tTime, fmt(Math.ceil(cdRemaining(countdown) - 1e-6)));
        setState(pv.timer, countdown.state);
      } else {
        setText(pv.tLabel, segLabel(seg) + (t ? ' · ' + fmt(t.dur) : '') + ' · 段落計時');
        setText(pv.tTime, timerText(t));
        setState(pv.timer, st);
      }
      setText($('[data-cmd="start"]', pv.timer), countdown && countdown.state === 'paused' || !countdown && t && !t.running && elapsedMs(t) > 0 ? '繼續' : '開始');
      var d = new Date();
      setText(pv.clockTime, pad2(d.getHours()) + ':' + pad2(d.getMinutes()) + ':' + pad2(d.getSeconds()));
      pv.wsBtn.textContent = workshopStart == null ? '開始工作坊' : '重新起算工作坊';
      var s = slides[i];
      var pm = s && s.hasAttribute('data-minute') ? parseInt(s.getAttribute('data-minute'), 10) : NaN;
      var planned = isNaN(pm) ? '--' : pad2(pm);
      var actualMin = workshopStart == null ? NaN : Math.floor((now() - workshopStart) / 60000);
      var actual = isNaN(actualMin) ? '--' : pad2(actualMin);
      setText(pv.plan, '計畫 第 ' + planned + ' 分 · 實際 第 ' + actual + ' 分');
      var drift = (!isNaN(pm) && !isNaN(actualMin)) ? actualMin - pm : 0;
      setState(pv.plan, isNaN(actualMin) ? 'idle' : (drift > 2 ? 'late' : (drift < -2 ? 'ahead' : 'ontime')));
      pv.plan.setAttribute('data-drift', String(drift));
      var op = null;
      try { op = window.opener; } catch (e) { op = null; }
      setText(pv.link, !op ? '獨立模式（未連到主簡報）' : (op.closed ? '主簡報已關閉' : (gotState ? '已同步' : '連線中…')));
    }

    /* ---------------- keys: T / R / P (core leaves these alone) ---------------- */
    document.addEventListener('keydown', function (e) {
      if (e.ctrlKey || e.metaKey || e.altKey || e.defaultPrevented) return;
      var tg = e.target;
      if (tg && (tg.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName || ''))) return;
      var k = (e.key || '').toLowerCase(), code = e.code || '';
      if (k === 't' || code === 'KeyT') {
        e.preventDefault();
        if (isPresenter) remote({ action: 'timer', cmd: 'toggle' }); else command('toggle');
      } else if (k === 'r' || code === 'KeyR') {
        e.preventDefault();
        if (isPresenter) remote({ action: 'timer', cmd: 'reset' }); else command('reset');
      } else if ((k === 'p' || code === 'KeyP') && !isPresenter) {
        e.preventDefault();
        openPresenter();
      }
    });

    /* ---------------- navigation events ---------------- */
    if (typeof DK.on === 'function') {
      DK.on('change', function () {
        if (isPresenter) {
          renderPresenterFull();
          var i = curIndex(), f = curFrag();
          if (!remoteApplying && gotState && (i !== lastRemote.index || f !== lastRemote.frag)) {
            lastRemote = { index: i, frag: f };
            remote({ action: 'go', index: i, frag: f });
          }
        } else {
          sendState(true);
        }
        renderAll();
      });
    }

    /* ---------------- start ---------------- */
    if (isPresenter) {
      buildPresenter();
      renderPresenterFull();
      var hellos = 0;
      var sayHello = function () {
        if (gotState || hellos > 40) return;
        hellos++;
        var op = null;
        try { op = window.opener; } catch (e) { op = null; }
        if (op && !op.closed) post(op, { type: 'dk', action: 'hello' });
        setTimeout(sayHello, 1000);
      };
      sayHello();
    }
    renderAll();
    setInterval(function () {
      renderAll();
      sendState(false);
    }, 250);

    /* debug / test hook */
    window.DKF = {
      timers: function () { return timers; },
      countdowns: function () { return countdowns; },
      workshopStart: function () { return workshopStart; },
      command: command,
      openPresenter: openPresenter
    };
  }
})();
