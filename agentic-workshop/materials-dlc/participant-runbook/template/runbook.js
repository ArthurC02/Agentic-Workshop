/*! Smart Ticket 工作坊 Runbook — runbook.js (plain ES2018, no external libraries, file:// safe) */
(function () {
  'use strict';

  var VERSION = '2.0.0';
  var doc = document;
  var root = doc.documentElement;

  /* ------------------------------------------------------------------ *
   * Small helpers
   * ------------------------------------------------------------------ */
  function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
  function el(tag, cls, text) {
    var e = doc.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function on(target, type, fn, opts) { if (target) target.addEventListener(type, fn, opts || false); }
  function debounce(fn, ms) {
    var t = null;
    return function () {
      var args = arguments, self = this;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(self, args); }, ms);
    };
  }
  function pad2(n) { return (n < 10 ? '0' : '') + n; }
  function nowHMS() { var d = new Date(); return pad2(d.getHours()) + ':' + pad2(d.getMinutes()) + ':' + pad2(d.getSeconds()); }

  /* ------------------------------------------------------------------ *
   * localStorage (every access guarded — file://, private mode, policies)
   * ------------------------------------------------------------------ */
  var store = {
    ok: (function () {
      try { var k = '{{STORAGE_PREFIX}}__probe'; localStorage.setItem(k, '1'); localStorage.removeItem(k); return true; } catch (e) { return false; }
    })(),
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, String(v)); return true; } catch (e) { return false; } },
    del: function (k) { try { localStorage.removeItem(k); } catch (e) { /* ignore */ } },
    getJSON: function (k) {
      var v = store.get(k);
      if (v == null) return null;
      try { return JSON.parse(v); } catch (e) { return null; }
    },
    setJSON: function (k, v) { try { return store.set(k, JSON.stringify(v)); } catch (e) { return false; } }
  };

  /* ------------------------------------------------------------------ *
   * Pure-JS SHA-256 (FIPS 180-4) over Uint8Array -> Uint8Array(32)
   * Must match Python hashlib.sha256 byte-for-byte.
   * ------------------------------------------------------------------ */
  var K256 = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
  ];
  var W256 = new Int32Array(64);

  function sha256(bytes) {
    var len = bytes.length;
    var total = Math.ceil((len + 9) / 64) * 64;
    var m = new Uint8Array(total);
    m.set(bytes);
    m[len] = 0x80;
    var bitsHi = Math.floor(len / 0x20000000);
    var bitsLo = (len * 8) >>> 0;
    m[total - 8] = (bitsHi >>> 24) & 255; m[total - 7] = (bitsHi >>> 16) & 255;
    m[total - 6] = (bitsHi >>> 8) & 255;  m[total - 5] = bitsHi & 255;
    m[total - 4] = (bitsLo >>> 24) & 255; m[total - 3] = (bitsLo >>> 16) & 255;
    m[total - 2] = (bitsLo >>> 8) & 255;  m[total - 1] = bitsLo & 255;

    var h0 = 0x6a09e667 | 0, h1 = 0xbb67ae85 | 0, h2 = 0x3c6ef372 | 0, h3 = 0xa54ff53a | 0,
        h4 = 0x510e527f | 0, h5 = 0x9b05688c | 0, h6 = 0x1f83d9ab | 0, h7 = 0x5be0cd19 | 0;
    var w = W256, i, t, a, b, c, d, e, f, g, h, s0, s1, t1, t2, x;

    for (var off = 0; off < total; off += 64) {
      for (i = 0; i < 16; i++) {
        t = off + i * 4;
        w[i] = (m[t] << 24) | (m[t + 1] << 16) | (m[t + 2] << 8) | m[t + 3];
      }
      for (i = 16; i < 64; i++) {
        x = w[i - 15];
        s0 = ((x >>> 7) | (x << 25)) ^ ((x >>> 18) | (x << 14)) ^ (x >>> 3);
        x = w[i - 2];
        s1 = ((x >>> 17) | (x << 15)) ^ ((x >>> 19) | (x << 13)) ^ (x >>> 10);
        w[i] = (w[i - 16] + s0 + w[i - 7] + s1) | 0;
      }
      a = h0; b = h1; c = h2; d = h3; e = h4; f = h5; g = h6; h = h7;
      for (i = 0; i < 64; i++) {
        s1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
        t1 = (h + s1 + ((e & f) ^ (~e & g)) + K256[i] + w[i]) | 0;
        s0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
        t2 = (s0 + ((a & b) ^ (a & c) ^ (b & c))) | 0;
        h = g; g = f; f = e; e = (d + t1) | 0;
        d = c; c = b; b = a; a = (t1 + t2) | 0;
      }
      h0 = (h0 + a) | 0; h1 = (h1 + b) | 0; h2 = (h2 + c) | 0; h3 = (h3 + d) | 0;
      h4 = (h4 + e) | 0; h5 = (h5 + f) | 0; h6 = (h6 + g) | 0; h7 = (h7 + h) | 0;
    }
    var out = new Uint8Array(32), hs = [h0, h1, h2, h3, h4, h5, h6, h7];
    for (i = 0; i < 8; i++) {
      out[i * 4] = (hs[i] >>> 24) & 255; out[i * 4 + 1] = (hs[i] >>> 16) & 255;
      out[i * 4 + 2] = (hs[i] >>> 8) & 255; out[i * 4 + 3] = hs[i] & 255;
    }
    return out;
  }

  function toHex(bytes) {
    var s = '';
    for (var i = 0; i < bytes.length; i++) s += (bytes[i] < 16 ? '0' : '') + bytes[i].toString(16);
    return s;
  }

  /* ------------------------------------------------------------------ *
   * UTF-8 / base64 helpers
   * ------------------------------------------------------------------ */
  var hasTE = typeof TextEncoder !== 'undefined';
  var hasTD = typeof TextDecoder !== 'undefined';

  function utf8Encode(str) {
    if (hasTE) return new TextEncoder().encode(str);
    var bin = unescape(encodeURIComponent(str));
    var out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  function utf8Decode(bytes) {
    if (hasTD) return new TextDecoder('utf-8').decode(bytes);
    var parts = [], CH = 0x8000;
    for (var i = 0; i < bytes.length; i += CH) {
      parts.push(String.fromCharCode.apply(null, bytes.subarray(i, i + CH)));
    }
    return decodeURIComponent(escape(parts.join('')));
  }

  function b64ToBytes(b64) {
    var bin = atob(String(b64 || '').replace(/[^A-Za-z0-9+/=]/g, ''));
    var n = bin.length, out = new Uint8Array(n);
    for (var i = 0; i < n; i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  function sha256Hex(str) { return toHex(sha256(utf8Encode(str))); }

  /* ------------------------------------------------------------------ *
   * Scheme B (obfuscation, identical to the Python builder)
   *   n         = uppercase(code) keeping only [A-Z0-9]
   *   verifier  = hex(SHA256("verify:" + salt + ":" + n))
   *   keystream = SHA256("ks:" + salt + ":" + n + ":" + i), i = 0,1,2…
   *   payload   = base64(utf8(json) XOR keystream)
   * ------------------------------------------------------------------ */
  function normalizeCode(code) { return String(code == null ? '' : code).toUpperCase().replace(/[^A-Z0-9]/g, ''); }

  function makeVerifier(salt, n) { return sha256Hex('verify:' + salt + ':' + n); }

  function decodePayload(salt, n, payloadB64) {
    var data = b64ToBytes(payloadB64);
    var prefix = 'ks:' + salt + ':' + n + ':';
    for (var off = 0, i = 0; off < data.length; off += 32, i++) {
      var ks = sha256(utf8Encode(prefix + i));
      var end = Math.min(32, data.length - off);
      for (var j = 0; j < end; j++) data[off + j] ^= ks[j];
    }
    return JSON.parse(utf8Decode(data));
  }

  /* ------------------------------------------------------------------ *
   * Data & state
   * ------------------------------------------------------------------ */
  var DATA = { pages: [], groups: [], build: {} };
  try {
    var dataEl = doc.getElementById('rb-data');
    if (dataEl) DATA = JSON.parse(dataEl.textContent || '{}') || DATA;
  } catch (e) { /* keep defaults; page still navigable */ }
  DATA.pages = DATA.pages || [];
  DATA.groups = DATA.groups || [];

  var pageById = {}, groupById = {};
  DATA.pages.forEach(function (p) { pageById[p.id] = p; });
  DATA.groups.forEach(function (g) { groupById[g.id] = g; });

  var unlocked = {};          // groupId -> true
  var downloadData = {};      // downloadId -> base64 zip
  if (DATA.downloads) Object.keys(DATA.downloads).forEach(function (k) { downloadData[k] = DATA.downloads[k]; });
  var currentId = null;

  var articles = {};          // pageId -> <article>
  $$('.rb-page[data-page]').forEach(function (a) {
    var id = a.getAttribute('data-page');
    articles[id] = a;
    if (!pageById[id]) {
      pageById[id] = { id: id, title: a.getAttribute('data-title') || id, section: a.getAttribute('data-section') || '',
        minute: a.getAttribute('data-minute') || '', group: a.getAttribute('data-group') || 'open' };
      DATA.pages.push(pageById[id]);
    }
  });
  var order = DATA.pages.map(function (p) { return p.id; }).filter(function (id) { return articles[id]; });
  var navLinks = $$('.rb-nav-link[data-page]');

  function pageGroup(id) {
    var p = pageById[id];
    if (p && p.group) return p.group;
    var a = articles[id];
    return (a && a.getAttribute('data-group')) || 'open';
  }
  function isPageLocked(id) {
    var g = pageGroup(id);
    return g !== 'open' && !unlocked[g];
  }
  function pageTitle(id) {
    var p = pageById[id];
    return (p && p.title) || (articles[id] && articles[id].getAttribute('data-title')) || id;
  }

  /* ------------------------------------------------------------------ *
   * Toasts
   * ------------------------------------------------------------------ */
  var toastsBox = $('.rb-toasts');
  function toast(msg, kind) {
    if (!toastsBox) return;
    var t = el('div', 'rb-toast rb-toast-' + (kind || 'info'), msg);
    toastsBox.appendChild(t);
    while (toastsBox.children.length > 3) toastsBox.removeChild(toastsBox.firstChild);   // never bury the page
    setTimeout(function () { t.classList.add('is-leaving'); }, 2800);
    setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 3300);
  }

  /* ------------------------------------------------------------------ *
   * Navigation / page head / TOC / pager
   * ------------------------------------------------------------------ */
  var titleEl = $('.rb-page-title'), metaEl = $('.rb-page-meta'), crumbEl = $('.rb-breadcrumb');
  var tocList = $('.rb-toc-list'), pagerEl = $('.rb-pager');
  var baseTitle = doc.title;

  function updateNavStates() {
    navLinks.forEach(function (a) {
      var id = a.getAttribute('data-page');
      var locked = isPageLocked(id);
      a.classList.toggle('is-current', id === currentId);
      a.classList.toggle('is-locked', locked);
      a.classList.toggle('is-done', !locked && pageDone(id));
      a.classList.toggle('is-unlocked', !locked && pageGroup(id) !== 'open');
      if (id === currentId) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    $$('a.rb-xref').forEach(function (x) {
      var m = /^#p-(.+)$/.exec(x.getAttribute('href') || '');
      var locked = !!(m && articles[m[1]] && isPageLocked(m[1]));
      x.classList.toggle('is-locked', locked);
      if (locked) x.setAttribute('title', '此章節尚未解鎖'); else x.removeAttribute('title');
    });
  }

  /* Steps: a task page with 2+ "檢查點 N · …（第 a–b 分鐘）" headings is split into
   * 總覽 + one step per top-level heading from the first checkpoint on; one step is
   * shown at a time and listed as sub-items under the page in the left nav. */
  var STEP_RE = /^檢查點\s*(\d+)\s*[·・]\s*(.*?)\s*（第\s*([0-9–-]+)\s*分鐘）\s*$/;
  var steps = {};             // pageId -> [{ id, label, min, el }]
  var stepMem = {};           // pageId -> current step id (works without localStorage)

  function buildSteps(art) {
    var pid = art.getAttribute('data-page'), body = art.querySelector('.rb-page-body');
    if (!body || body.querySelector(':scope > .rb-step')) return;     // already split
    delete steps[pid];
    var heads = $$(':scope > h3[id]', body);
    if (heads.filter(function (h) { return STEP_RE.test(h.textContent.trim()); }).length < 2) return;
    var list = [], cur = null, started = false;
    function open(id, label, min) {
      cur = { id: id, label: label, min: min, el: el('section', 'rb-step') };
      cur.el.setAttribute('data-step', id);
      list.push(cur);
    }
    open(pid + '--overview', '總覽', '');
    cur.el.id = pid + '--overview';
    Array.prototype.slice.call(body.childNodes).forEach(function (n) {
      if (n.nodeType === 1 && n.tagName === 'H3' && n.id) {
        var m = STEP_RE.exec(n.textContent.trim());
        if (m) started = true;
        if (started) open(n.id, m ? m[1] + ' · ' + m[2] : n.textContent.trim(), m ? m[3] : '');
      }
      cur.el.appendChild(n);
    });
    list.forEach(function (s) { body.appendChild(s.el); });
    steps[pid] = list;
  }

  function stepIndex(id) {
    var list = steps[id];
    if (!list) return -1;
    var want = stepMem[id] || store.get('{{STORAGE_PREFIX}}step:' + id);
    for (var i = 0; i < list.length; i++) if (list[i].id === want) return i;
    return 0;
  }

  function showStep(id, i) {
    var list = steps[id];
    if (!list) return;
    list.forEach(function (s, k) { s.el.hidden = k !== i; });
    stepMem[id] = list[i].id;
    store.set('{{STORAGE_PREFIX}}step:' + id, list[i].id);
  }

  function renderNavSteps() {
    $$('.rb-nav-steps').forEach(function (n) { n.parentNode.removeChild(n); });
    var list = steps[currentId];
    var link = list && !isPageLocked(currentId) && $('.rb-nav-link[data-page="' + currentId + '"]');
    if (!link) return;
    var cur = stepIndex(currentId);
    var ol = el('ol', 'rb-nav-steps');
    ol.setAttribute('aria-label', pageTitle(currentId) + '：步驟');
    list.forEach(function (s, k) {
      var a = el('a', 'rb-nav-step' + (k === cur ? ' is-current' : ''));
      a.href = '#' + s.id;
      a.appendChild(el('span', 'rb-nav-step-title', s.label));
      if (s.min) a.appendChild(el('span', 'rb-badge rb-badge-min', s.min));
      if (k === cur) a.setAttribute('aria-current', 'step');
      var li = el('li');
      li.appendChild(a);
      ol.appendChild(li);
    });
    link.parentNode.appendChild(ol);
  }

  function renderHead(id) {
    var p = pageById[id] || {};
    var locked = isPageLocked(id);
    if (titleEl) titleEl.textContent = pageTitle(id);
    if (crumbEl) {
      crumbEl.innerHTML = '';
      if (p.section) {
        crumbEl.appendChild(el('span', 'rb-crumb', p.section));
      }
      var cur = el('span', 'rb-crumb rb-crumb-current is-current', pageTitle(id));
      cur.setAttribute('aria-current', 'page');
      crumbEl.appendChild(cur);
    }
    if (metaEl) {
      metaEl.innerHTML = '';
      if (p.minute !== undefined && p.minute !== '') metaEl.appendChild(el('span', 'rb-meta-item rb-meta-min', String(p.minute)));
      var idx = order.indexOf(id);
      metaEl.appendChild(el('span', 'rb-meta-item', '第 ' + (idx + 1) + ' / ' + order.length + ' 章'));
      if (steps[id] && !locked) metaEl.appendChild(el('span', 'rb-meta-item rb-meta-step', '第 ' + (stepIndex(id) + 1) + ' / ' + steps[id].length + ' 步'));
      if (pageGroup(id) !== 'open') {
        metaEl.appendChild(el('span', 'rb-meta-item ' + (locked ? 'is-locked' : 'is-unlocked'), locked ? '尚未解鎖' : '已解鎖'));
      }
      if (!locked && pageDone(id)) metaEl.appendChild(el('span', 'rb-meta-item is-done', '已完成'));
    }
    doc.title = pageTitle(id) + ' · ' + baseTitle;
  }

  var tocObserver = null;
  function renderToc(id) {
    if (!tocList) return;
    tocList.innerHTML = '';
    if (tocObserver) { tocObserver.disconnect(); tocObserver = null; }
    var art = articles[id];
    var hs = art ? $$('.rb-page-body h2[id], .rb-page-body h3[id]', art) : [];
    var sub = 'H3';
    if (steps[id]) {
      var stepEl = steps[id][stepIndex(id)].el;
      hs = $$('h3[id], h4[id]', stepEl).filter(function (h) { return !h.closest('.rb-include'); });
      sub = 'H4';
    }
    var tocBox = $('.rb-toc');
    if (tocBox) tocBox.classList.toggle('is-empty', hs.length === 0);
    if (!hs.length) {
      if (isPageLocked(id)) tocList.appendChild(el('li', 'rb-toc-empty', '解鎖後顯示'));
      return;
    }
    var linkFor = {};
    hs.forEach(function (h) {
      var li = el('li', 'rb-toc-item' + (h.tagName === sub ? ' rb-toc-sub rb-toc-h3' : ''));
      li.setAttribute('data-level', h.tagName.charAt(1));
      var a = el('a', 'rb-toc-link', h.textContent);
      a.href = '#' + h.id;
      a.setAttribute('data-level', h.tagName.charAt(1));
      on(a, 'click', function (ev) {
        ev.preventDefault();
        scrollToEl(h);
        try { history.replaceState(null, '', '#' + h.id); } catch (e) { /* file:// quirks */ }
      });
      li.appendChild(a);
      tocList.appendChild(li);
      linkFor[h.id] = a;
    });
    if ('IntersectionObserver' in window) {
      tocObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          $$('.rb-toc-link.is-active', tocList).forEach(function (x) { x.classList.remove('is-active'); });
          var l = linkFor[en.target.id];
          if (l) l.classList.add('is-active');
        });
      }, { rootMargin: '-72px 0px -70% 0px', threshold: 0 });
      hs.forEach(function (h) { tocObserver.observe(h); });
    }
  }

  function pagerLink(id, dir) {
    var a = el('a', 'rb-pager-link rb-pager-' + dir + (isPageLocked(id) ? ' is-locked' : ''));
    a.href = '#p-' + id;
    a.appendChild(el('span', 'rb-pager-dir', dir === 'prev' ? '上一頁' : '下一頁'));
    a.appendChild(el('span', 'rb-pager-title', pageTitle(id)));
    return a;
  }
  function stepLink(s, dir) {
    var a = el('a', 'rb-pager-link rb-pager-' + dir);
    a.href = '#' + s.id;
    a.appendChild(el('span', 'rb-pager-dir', dir === 'prev' ? '上一步' : '下一步'));
    a.appendChild(el('span', 'rb-pager-title', s.label));
    return a;
  }
  function renderPager(id) {
    if (!pagerEl) return;
    pagerEl.innerHTML = '';
    var list = !isPageLocked(id) && steps[id], k = list ? stepIndex(id) : -1;
    if (list && (k > 0 || k < list.length - 1)) {
      if (k > 0) pagerEl.appendChild(stepLink(list[k - 1], 'prev'));
      else if (order.indexOf(id) > 0) pagerEl.appendChild(pagerLink(order[order.indexOf(id) - 1], 'prev'));
      if (k < list.length - 1) pagerEl.appendChild(stepLink(list[k + 1], 'next'));
      else if (order.indexOf(id) < order.length - 1) pagerEl.appendChild(pagerLink(order[order.indexOf(id) + 1], 'next'));
      return;
    }
    var i = order.indexOf(id);
    if (i > 0) pagerEl.appendChild(pagerLink(order[i - 1], 'prev'));
    if (i >= 0 && i < order.length - 1) pagerEl.appendChild(pagerLink(order[i + 1], 'next'));
  }

  function scrollToEl(target) {
    try { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); } catch (e) { target.scrollIntoView(true); }
  }

  function showPage(id, anchorEl) {
    if (!articles[id]) id = order[0];
    if (!id) return;
    var changed = id !== currentId;
    Object.keys(articles).forEach(function (k) { articles[k].hidden = (k !== id); });
    currentId = id;
    store.set('{{STORAGE_PREFIX}}last-page', id);
    if (steps[id]) {
      var stepEl = anchorEl && anchorEl.closest ? anchorEl.closest('.rb-step') : null;
      var k = stepEl ? steps[id].map(function (s) { return s.el; }).indexOf(stepEl) : -1;
      var before = stepIndex(id);
      showStep(id, k >= 0 ? k : before);
      if (k >= 0 && k !== before) changed = true;
      // Jumping to a step itself (its section or its heading) starts at the top.
      if (stepEl && (anchorEl === stepEl || anchorEl === stepEl.firstElementChild)) anchorEl = null;
    }
    renderHead(id);
    renderToc(id);
    renderPager(id);
    updateNavStates();
    renderNavSteps();
    closeSidebar();
    if (anchorEl) setTimeout(function () { scrollToEl(anchorEl); }, 0);
    else if (changed) { resetScroll(); setTimeout(resetScroll, 0); }
  }

  // The browser's native jump to #p-<id> would scroll the article (and any
  // overflow container around it) past the page head; undo that on every page change.
  function resetScroll() {
    var art = articles[currentId];
    for (var n = art ? art.parentElement : null; n; n = n.parentElement) { if (n.scrollTop) n.scrollTop = 0; }
    try { window.scrollTo(0, 0); } catch (e) { /* ignore */ }
  }

  // Folded tips (<details class="rb-callout-fold">): open every fold around a node so a jump can land in it.
  function revealFolds(node) {
    for (var d = node && node.closest ? node.closest('details') : null; d; d = d.parentElement ? d.parentElement.closest('details') : null) d.open = true;
  }

  // After a search jump: open folds holding the query; scroll to one when the first hit lies inside it.
  function revealSearchHit(q) {
    var art = articles[currentId];
    if (!art || !q) return;
    var scope = art.querySelector('.rb-step:not([hidden])') || art;
    $$('details.rb-callout-fold', scope).forEach(function (d) {
      if ((d.textContent || '').toLowerCase().indexOf(q) >= 0) d.open = true;
    });
    var walker = doc.createTreeWalker(scope, NodeFilter.SHOW_TEXT, null), n;
    while ((n = walker.nextNode())) {
      if ((n.nodeValue || '').toLowerCase().indexOf(q) < 0) continue;
      var fold = n.parentElement && n.parentElement.closest('details.rb-callout-fold');
      if (fold) scrollToEl(fold);
      return;
    }
  }

  function initFolds() {
    var opened = [];
    on(window, 'beforeprint', function () {
      opened = $$('details.rb-callout-fold:not([open])');
      opened.forEach(function (d) { d.open = true; });
    });
    on(window, 'afterprint', function () {
      opened.forEach(function (d) { d.open = false; });
      opened = [];
    });
  }

  function route() {
    var raw = (location.hash || '').slice(1), h = raw;
    try { h = decodeURIComponent(raw); } catch (e) { h = raw; }
    if (h.indexOf('p-') === 0 && articles[h.slice(2)]) { showPage(h.slice(2)); return; }
    if (h) {
      var target = doc.getElementById(h);
      var art = target && target.closest ? target.closest('.rb-page') : null;
      if (art) { revealFolds(target); showPage(art.getAttribute('data-page'), target); return; }
    }
    var last = store.get('{{STORAGE_PREFIX}}last-page');
    showPage(last && articles[last] ? last : order[0]);
  }

  /* ------------------------------------------------------------------ *
   * Clipboard (async API with textarea fallback for file:// / older policies)
   * ------------------------------------------------------------------ */
  function fallbackCopy(text) {
    var ta = el('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed'; ta.style.top = '-1000px'; ta.style.opacity = '0';
    doc.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = doc.execCommand('copy'); } catch (e) { ok = false; }
    doc.body.removeChild(ta);
    return ok;
  }
  function copyText(text) {
    return new Promise(function (resolve) {
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () { resolve(true); }, function () { resolve(fallbackCopy(text)); });
          return;
        }
      } catch (e) { /* fall through */ }
      resolve(fallbackCopy(text));
    });
  }

  function saveBlob(blob, filename) {
    try {
      if (window.navigator && window.navigator.msSaveOrOpenBlob) { window.navigator.msSaveOrOpenBlob(blob, filename); return true; }
      var url = URL.createObjectURL(blob);
      var a = el('a');
      a.href = url; a.download = filename; a.style.display = 'none';
      doc.body.appendChild(a);
      a.click();
      setTimeout(function () { doc.body.removeChild(a); URL.revokeObjectURL(url); }, 30000);
      return true;
    } catch (e) { return false; }
  }

  // Included source documents: copy the original Markdown or save it as a .md file.
  function initIncludes(ctx) {
    $$('.rb-include-meta', ctx).forEach(function (meta) {
      var src = meta.querySelector(':scope > .rb-include-src');
      if (!src || meta.querySelector(':scope > .rb-include-actions')) return;
      var md, name = (meta.querySelector('code') || {}).textContent || 'document.md';
      try { md = JSON.parse(src.textContent); } catch (e) { return; }
      var box = meta.appendChild(el('span', 'rb-include-actions'));
      var copy = box.appendChild(el('button', 'rb-chip', '複製 Markdown'));
      copy.type = 'button';
      on(copy, 'click', function () {
        copyText(md).then(function (ok) {
          toast(ok ? '已複製 ' + name : '無法存取剪貼簿，請改用下載', ok ? 'info' : 'warning');
        });
      });
      var dl = box.appendChild(el('button', 'rb-chip', '下載 .md'));
      dl.type = 'button';
      on(dl, 'click', function () {
        if (!saveBlob(new Blob([md], { type: 'text/markdown;charset=utf-8' }), name)) toast('下載失敗', 'warning');
      });
    });
  }

  /* ------------------------------------------------------------------ *
   * Components: copy buttons, cmd tabs, task checkboxes, downloads, forms
   * ------------------------------------------------------------------ */
  function initCopy(ctx) {
    $$('pre.rb-code', ctx).forEach(function (pre) {
      // The button lives in a .rb-code-wrap around the <pre> (not inside it), so it
      // stays put when the code scrolls horizontally.
      var wrap = pre.parentNode;
      if (!wrap || !wrap.classList || !wrap.classList.contains('rb-code-wrap')) {
        wrap = el('div', 'rb-code-wrap');
        pre.parentNode.insertBefore(wrap, pre);
        wrap.appendChild(pre);
      }
      if (wrap.querySelector(':scope > .rb-copy')) return;
      var btn = el('button', 'rb-copy', '複製');
      btn.type = 'button';
      btn.setAttribute('aria-label', '複製程式碼');
      on(btn, 'click', function () {
        var code = pre.querySelector('code');
        copyText((code || pre).textContent.replace(/\n$/, '')).then(function (ok) {
          btn.textContent = ok ? '已複製' : '複製失敗';
          btn.classList.toggle('is-copied', ok);
          btn.classList.toggle('is-error', !ok);
          if (!ok) toast('無法存取剪貼簿，請手動選取複製', 'warning');
          setTimeout(function () { btn.textContent = '複製'; btn.classList.remove('is-copied'); }, 1600);
        });
      });
      wrap.appendChild(btn);
    });
  }

  // Tabbed blocks: ```cmd (shell: powershell/bash) and ```prompt (os: windows/macos).
  // The choice is remembered per kind and applied to every block of that kind on all pages.
  var tabMem = {};  // fallback when localStorage is unavailable
  function tabKind(box) { return box.classList.contains('rb-prompt') ? 'os' : 'shell'; }
  function defaultTab(kind) {
    var s = store.get('{{STORAGE_PREFIX}}' + kind) || tabMem[kind];
    if (kind === 'os' ? (s === 'windows' || s === 'macos') : (s === 'powershell' || s === 'bash')) return s;
    var plat = (navigator.userAgentData && navigator.userAgentData.platform) || navigator.platform || '';
    if (kind === 'os') return /mac/i.test(plat) ? 'macos' : 'windows';
    return /win/i.test(plat) ? 'powershell' : 'bash';
  }
  function applyTab(kind, value, ctx) {
    $$('.rb-cmd', ctx).forEach(function (box) {
      if (tabKind(box) !== kind) return;
      var tabs = $$('.rb-cmd-tab', box);
      if (!tabs.length) return;
      var has = tabs.some(function (t) { return t.getAttribute('data-shell') === value; });
      var use = has ? value : tabs[0].getAttribute('data-shell');
      tabs.forEach(function (t) {
        var act = t.getAttribute('data-shell') === use;
        t.classList.toggle('is-active', act);
        t.setAttribute('aria-selected', act ? 'true' : 'false');
        t.setAttribute('role', 'tab');
        t.tabIndex = act ? 0 : -1;
      });
      $$('pre[data-shell]', box).forEach(function (p) { p.hidden = p.getAttribute('data-shell') !== use; });
    });
  }
  function chooseTab(kind, value) {
    tabMem[kind] = value;
    store.set('{{STORAGE_PREFIX}}' + kind, value);
    applyTab(kind, value, doc);
  }
  function initCmd(ctx) {
    $$('.rb-cmd', ctx).forEach(function (box) {
      if (box.getAttribute('data-rb-init')) return;
      box.setAttribute('data-rb-init', '1');
      var kind = tabKind(box), tabs = $$('.rb-cmd-tab', box);
      tabs.forEach(function (t, i) {
        on(t, 'click', function () { chooseTab(kind, t.getAttribute('data-shell')); });
        on(t, 'keydown', function (ev) {
          var j = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[ev.key];
          if (j === undefined) return;
          ev.preventDefault();
          var next = tabs[(j + tabs.length) % tabs.length];
          chooseTab(kind, next.getAttribute('data-shell'));
          next.focus();
        });
      });
    });
    applyTab('shell', defaultTab('shell'), ctx);
    applyTab('os', defaultTab('os'), ctx);
  }

  function initChecks(ctx) {
    $$('input.rb-check[data-check]', ctx).forEach(function (cb) {
      if (cb.getAttribute('data-rb-init')) return;
      cb.setAttribute('data-rb-init', '1');
      var key = '{{STORAGE_PREFIX}}check:' + cb.getAttribute('data-check');
      cb.checked = store.get(key) === '1';
      var li = cb.closest ? cb.closest('.rb-task') : null;
      if (li) li.classList.toggle('is-checked', cb.checked);
      on(cb, 'change', function () {
        if (cb.checked) store.set(key, '1'); else store.del(key);
        if (li) li.classList.toggle('is-checked', cb.checked);
        updateProgress();
      });
    });
  }

  function pageDone(id) {
    var art = articles[id];
    if (!art) return false;
    var cbs = $$('input.rb-check', art);
    return cbs.length > 0 && cbs.every(function (c) { return c.checked; });
  }

  var progEl = $('.rb-progress'), progFill = $('.rb-progress-fill'), progNum = $('.rb-progress-num');
  function updateProgress() {
    var all = $$('.rb-page input.rb-check');   // locked pages carry no checkboxes in the DOM
    var done = all.filter(function (c) { return c.checked; }).length;
    var pct = all.length ? Math.round(done * 100 / all.length) : 0;
    if (progFill) progFill.style.width = pct + '%';
    if (progNum) progNum.textContent = pct + '%';
    if (progEl) {
      progEl.setAttribute('aria-valuenow', String(pct));
      progEl.setAttribute('title', '已完成 ' + done + ' / ' + all.length + ' 項任務');
    }
    if (currentId) renderHead(currentId);
    updateNavStates();
  }

  function initDownloads(ctx) {
    $$('button.rb-download[data-download]', ctx).forEach(function (btn) {
      if (btn.getAttribute('data-rb-init')) return;
      btn.setAttribute('data-rb-init', '1');
      on(btn, 'click', function () {
        var id = btn.getAttribute('data-download');
        var name = btn.getAttribute('data-filename') || (id + '.zip');
        var b64 = downloadData[id];
        if (!b64) { toast('找不到此下載內容（可能尚未解鎖）', 'danger'); return; }
        try {
          var ok = saveBlob(new Blob([b64ToBytes(b64)], { type: 'application/zip' }), name);
          if (ok) btn.classList.add('is-done');
          toast(ok ? '已下載 ' + name : '瀏覽器阻擋了下載', ok ? 'info' : 'danger');
        } catch (e) { toast('下載失敗：' + (e && e.message ? e.message : e), 'danger'); }
      });
    });
  }

  /* ------------------------------------------------------------------ *
   * Forms (autosave to stw:form:<id>, export / copy Markdown, two-step clear)
   * ------------------------------------------------------------------ */
  function fieldDefault(f) {
    if (f.type === 'checklist') {
      var items = f.items || f.options || [];
      var v = Array.isArray(f.value) ? f.value : [];
      return items.map(function (_, i) { return !!v[i]; });
    }
    if (f.type === 'checkbox') return !!f.value;
    return f.value != null ? String(f.value) : '';
  }

  function formToMarkdown(def, values) {
    var out = ['# ' + (def.title || def.id), ''];
    (def.fields || []).forEach(function (f) {
      var v = values[f.id];
      if (f.type === 'checkbox') {
        out.push('- [' + (v ? 'x' : ' ') + '] ' + f.label, '');
        return;
      }
      out.push('## ' + f.label, '');
      if (f.type === 'checklist') {
        (f.items || f.options || []).forEach(function (item, i) {
          out.push('- [' + (v && v[i] ? 'x' : ' ') + '] ' + item);
        });
        out.push('');
      } else {
        var s = v == null ? '' : String(v).replace(/\s+$/, '');
        out.push(s ? s : '（未填）', '');
      }
    });
    return out.join('\n').replace(/\n+$/, '') + '\n';
  }

  /* Capsule buttons: click inserts preset text (appended on a new line in textareas;
     replaces a text input's value) and saves through the field's normal input handler. */
  function suggestChips(f, inp) {
    var box = el('div', 'rb-suggest');
    box.setAttribute('role', 'group');
    box.setAttribute('aria-label', f.label + '：快速填入');
    f.suggestions.forEach(function (s) {
      var label = typeof s === 'string' ? s : s.label;
      var text = typeof s === 'string' ? s : s.text;
      var b = el('button', 'rb-chip', label);
      b.type = 'button';
      b.title = text;
      on(b, 'click', function () {
        if (inp.tagName === 'TEXTAREA' && inp.value.trim()) inp.value = inp.value.replace(/\s*$/, '') + '\n' + text;
        else inp.value = text;
        inp.dispatchEvent(new Event('input', { bubbles: true }));
        // ponytail: CSS field-sizing auto-grows in Chromium; elsewhere grow once here.
        if (inp.tagName === 'TEXTAREA' && inp.scrollHeight > inp.clientHeight) inp.style.height = (inp.scrollHeight + 4) + 'px';
        try {
          inp.focus();
          var p = inp.value.indexOf('〈', inp.value.length - text.length);
          if (p >= 0) inp.setSelectionRange(p, inp.value.indexOf('〉', p) + 1);
        } catch (e) { /* ignore */ }
      });
      box.appendChild(b);
    });
    return box;
  }

  /* Export all: every rendered form, one .md per form, foldered by page, as a ZIP. */
  var allForms = {};          // formId -> { def, values, page }

  function formHasInput(def, values) {
    return (def.fields || []).some(function (f) {
      var v = values[f.id];
      if (f.readonly) return false;
      if (Array.isArray(v)) return v.some(Boolean);
      return f.type === 'checkbox' ? !!v : String(v == null ? '' : v).trim() !== '';
    });
  }

  var crcTable = null;
  function crc32(b) {
    if (!crcTable) {
      crcTable = [];
      for (var n = 0; n < 256; n++) {
        var c = n;
        for (var k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1;
        crcTable[n] = c >>> 0;
      }
    }
    var x = -1;
    for (var i = 0; i < b.length; i++) x = crcTable[(x ^ b[i]) & 255] ^ (x >>> 8);
    return (x ^ -1) >>> 0;
  }

  // ponytail: stored (uncompressed) ZIP; a few KB of Markdown needs no deflate.
  function makeZip(files) {
    var parts = [], central = [], off = 0, d = new Date();
    var time = (d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1);
    var date = ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
    files.forEach(function (f) {
      var name = utf8Encode(f.name), data = utf8Encode(f.text), crc = crc32(data);
      var h = new DataView(new ArrayBuffer(30));
      h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint16(6, 0x0800, true);
      h.setUint16(10, time, true); h.setUint16(12, date, true); h.setUint32(14, crc, true);
      h.setUint32(18, data.length, true); h.setUint32(22, data.length, true); h.setUint16(26, name.length, true);
      parts.push(h.buffer, name, data);
      var c = new DataView(new ArrayBuffer(46));
      c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint16(8, 0x0800, true);
      c.setUint16(12, time, true); c.setUint16(14, date, true); c.setUint32(16, crc, true);
      c.setUint32(20, data.length, true); c.setUint32(24, data.length, true); c.setUint16(28, name.length, true);
      c.setUint32(42, off, true);
      central.push(c.buffer, name);
      off += 30 + name.length + data.length;
    });
    var size = 0;
    central.forEach(function (p) { size += p.byteLength; });
    var e = new DataView(new ArrayBuffer(22));
    e.setUint32(0, 0x06054b50, true); e.setUint16(8, files.length, true); e.setUint16(10, files.length, true);
    e.setUint32(12, size, true); e.setUint32(16, off, true);
    return new Blob(parts.concat(central, [e.buffer]), { type: 'application/zip' });
  }

  function exportAll() {
    var d = new Date(), stamp = d.getFullYear() + pad2(d.getMonth() + 1) + pad2(d.getDate()) + '-' + pad2(d.getHours()) + pad2(d.getMinutes());
    var files = [], index = ['# Smart Ticket 工作坊：填寫內容匯出', '', '匯出時間：' + d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate()) + ' ' + nowHMS(), ''];
    var empty = [];
    order.forEach(function (pid, i) {
      var mine = Object.keys(allForms).filter(function (fid) { return allForms[fid].page === pid; });
      var filled = mine.filter(function (fid) { return formHasInput(allForms[fid].def, allForms[fid].values); });
      mine.forEach(function (fid) { if (filled.indexOf(fid) < 0) empty.push(pageTitle(pid) + '：' + (allForms[fid].def.title || fid)); });
      if (!filled.length) return;
      var dir = pad2(i + 1) + '-' + pid + '/';
      index.push('## ' + pageTitle(pid), '');
      filled.forEach(function (fid) {
        files.push({ name: dir + fid + '.md', text: formToMarkdown(allForms[fid].def, allForms[fid].values) });
        index.push('- [' + (allForms[fid].def.title || fid) + '](' + dir + fid + '.md)');
      });
      index.push('');
    });
    if (!files.length) { toast('目前沒有任何已填寫的表單', 'warning'); return; }
    if (empty.length) index.push('## 未填寫（未匯出）', '', empty.map(function (s) { return '- ' + s; }).join('\n'), '');
    files.unshift({ name: 'README.md', text: index.join('\n') });
    var ok = saveBlob(makeZip(files), 'smart-ticket-dlc-runbook-' + stamp + '.zip');
    toast(ok ? '已下載 ' + (files.length - 1) + ' 份表單（ZIP）' : '瀏覽器阻擋了下載，請改用各表單的「匯出 Markdown」', ok ? 'info' : 'danger');
  }

  function initExportAll(ctx) {
    $$('.rb-export-all', ctx).forEach(function (box) {
      if (box.firstChild) return;
      var b = el('button', 'rb-btn rb-btn-primary', '下載全部填寫內容（ZIP）');
      b.type = 'button';
      on(b, 'click', exportAll);
      box.appendChild(b);
      box.appendChild(el('span', 'rb-field-hint', '每份已填寫的表單各一個 .md 檔，依章節分資料夾，附 README 目錄。'));
    });
  }

  function initForm(host) {
    if (host.getAttribute('data-rb-init')) return;
    var defEl = host.querySelector('script.rb-form-def');
    var def;
    try { def = JSON.parse(defEl ? defEl.textContent : ''); } catch (e) {
      host.appendChild(el('p', 'rb-field-hint', '表單定義無法解析。'));
      return;
    }
    host.setAttribute('data-rb-init', '1');
    var fid = def.id || host.getAttribute('data-form-id') || 'form';
    var key = '{{STORAGE_PREFIX}}form:' + fid;
    var saved = store.getJSON(key) || {};
    var values = {}, inputs = {};
    var fields = def.fields || [];
    var pageEl = host.closest ? host.closest('.rb-page') : null;
    allForms[fid] = { def: def, values: values, page: pageEl ? pageEl.getAttribute('data-page') : '' };

    var card = el('div', 'rb-form-card' + (def.kind ? ' rb-form-' + def.kind : ''));
    if (def.kind) card.setAttribute('data-kind', def.kind);
    card.appendChild(el('h3', 'rb-form-title', def.title || fid));
    var savedEl = el('span', 'rb-form-saved', saved && Object.keys(saved).length ? '已載入先前內容' : '');

    var persist = debounce(function () {
      var ok = store.setJSON(key, values);
      savedEl.textContent = ok ? '已自動儲存 ' + nowHMS() : '無法儲存（瀏覽器封鎖本機儲存）';
      savedEl.classList.toggle('is-error', !ok);
      savedEl.classList.remove('is-saving');
      savedEl.classList.add('is-flash');
      setTimeout(function () { savedEl.classList.remove('is-flash'); }, 1200);
    }, 400);

    fields.forEach(function (f) {
      var domId = 'rbf-' + fid + '-' + f.id;
      var wrap = el('div', 'rb-field rb-field-' + (f.type || 'text'));
      var initial = fieldDefault(f);
      if (!f.readonly && Object.prototype.hasOwnProperty.call(saved, f.id)) initial = saved[f.id];
      if (f.type === 'checklist') {
        var items = f.items || f.options || [];
        if (!Array.isArray(initial)) initial = items.map(function () { return false; });
        values[f.id] = items.map(function (_, i) { return !!initial[i]; });
        wrap.appendChild(el('label', 'rb-field-label', f.label));
        var list = el('div', 'rb-checklist');
        list.setAttribute('role', 'group');
        list.setAttribute('aria-label', f.label);
        var boxes = [];
        items.forEach(function (item, i) {
          var lab = el('label');
          var cb = el('input');
          cb.type = 'checkbox';
          cb.checked = values[f.id][i];
          if (f.readonly) cb.disabled = true;
          on(cb, 'change', function () { values[f.id][i] = cb.checked; persist(); });
          lab.appendChild(cb);
          lab.appendChild(el('span', null, item));
          list.appendChild(lab);
          boxes.push(cb);
        });
        inputs[f.id] = boxes;
        wrap.appendChild(list);
      } else if (f.type === 'checkbox') {
        values[f.id] = !!initial;
        var list1 = el('div', 'rb-checklist');
        var lab1 = el('label', 'rb-field-check');
        var cb1 = el('input');
        cb1.type = 'checkbox'; cb1.id = domId; cb1.checked = values[f.id];
        if (f.readonly) cb1.disabled = true;
        on(cb1, 'change', function () { values[f.id] = cb1.checked; persist(); });
        lab1.appendChild(cb1);
        lab1.appendChild(el('span', 'rb-field-label', f.label));
        list1.appendChild(lab1);
        inputs[f.id] = cb1;
        wrap.appendChild(list1);
      } else {
        var lbl = el('label', 'rb-field-label', f.label);
        lbl.setAttribute('for', domId);
        wrap.appendChild(lbl);
        var inp;
        if (f.type === 'textarea') {
          inp = el('textarea');
          inp.rows = 4;
        } else if (f.type === 'select') {
          inp = el('select');
          var o0 = el('option', null, '— 請選擇 —');
          o0.value = '';
          inp.appendChild(o0);
          (f.options || []).forEach(function (opt) {
            var o = el('option', null, String(opt));
            o.value = String(opt);
            inp.appendChild(o);
          });
          if ((f.options || []).map(String).indexOf(String(initial)) < 0) initial = '';
        } else {
          inp = el('input');
          inp.type = 'text';
          inp.autocomplete = 'off';
        }
        inp.id = domId;
        inp.name = f.id;
        inp.value = initial == null ? '' : String(initial);
        if (f.readonly) { inp.readOnly = true; if (f.type === 'select') inp.disabled = true; inp.classList.add('is-readonly'); }
        values[f.id] = inp.value;
        on(inp, f.type === 'select' ? 'change' : 'input', function () { values[f.id] = inp.value; persist(); });
        inputs[f.id] = inp;
        wrap.appendChild(inp);
        if (Array.isArray(f.suggestions) && !f.readonly) wrap.appendChild(suggestChips(f, inp));
      }
      if (f.hint) wrap.appendChild(el('p', 'rb-field-hint', f.hint));
      card.appendChild(wrap);
    });

    var actions = el('div', 'rb-form-actions');
    var bExport = el('button', 'rb-btn rb-btn-primary', '匯出 Markdown');
    var bCopy = el('button', 'rb-btn', '複製 Markdown');
    var bClear = el('button', 'rb-btn rb-btn-danger', '清除');
    [bExport, bCopy, bClear].forEach(function (b) { b.type = 'button'; actions.appendChild(b); });
    actions.appendChild(savedEl);
    card.appendChild(actions);

    on(bExport, 'click', function () {
      var md = formToMarkdown(def, values);
      var ok = saveBlob(new Blob([md], { type: 'text/markdown;charset=utf-8' }), fid + '.md');
      toast(ok ? '已匯出 ' + fid + '.md' : '瀏覽器阻擋了下載，請改用「複製 Markdown」', ok ? 'info' : 'danger');
    });
    on(bCopy, 'click', function () {
      copyText(formToMarkdown(def, values)).then(function (ok) {
        toast(ok ? '已複製 Markdown 到剪貼簿' : '無法存取剪貼簿', ok ? 'info' : 'danger');
      });
    });
    var clearTimer = null;
    function resetClear() {
      clearTimeout(clearTimer);
      bClear.textContent = '清除';
      bClear.classList.remove('is-confirm');
    }
    on(bClear, 'click', function () {
      if (!bClear.classList.contains('is-confirm')) {
        bClear.textContent = '確定清除？再按一次';
        bClear.classList.add('is-confirm');
        clearTimer = setTimeout(resetClear, 4000);
        return;
      }
      resetClear();
      store.del(key);
      fields.forEach(function (f) {
        var d = fieldDefault(f), ctl = inputs[f.id];
        values[f.id] = d;
        if (f.type === 'checklist') ctl.forEach(function (cb, i) { cb.checked = !!d[i]; });
        else if (f.type === 'checkbox') ctl.checked = !!d;
        else ctl.value = d;
      });
      savedEl.textContent = '已清除';
      toast('已清除表單「' + (def.title || fid) + '」');
    });
    on(bClear, 'blur', function () { setTimeout(resetClear, 150); });

    host.appendChild(card);
  }

  function initForms(ctx) { $$('.rb-form', ctx).forEach(initForm); }

  // Wide tables: flag the wrapper while it overflows so CSS can show the scroll hint.
  function markScroll(w) { w.classList.toggle('is-scrollable', w.scrollWidth > w.clientWidth + 2); }
  var tableRO = 'ResizeObserver' in window ? new ResizeObserver(function (es) { es.forEach(function (e) { markScroll(e.target); }); }) : null;
  function initTables(ctx) {
    $$('.rb-table-wrap', ctx).forEach(function (w) {
      if (w.getAttribute('data-rb-init')) return;
      w.setAttribute('data-rb-init', '1');
      if (tableRO) tableRO.observe(w); else markScroll(w);
    });
  }

  function initComponents(ctx) {
    initCopy(ctx);
    initIncludes(ctx);
    initCmd(ctx);
    initChecks(ctx);
    initForms(ctx);
    initExportAll(ctx);
    initTables(ctx);
    initDownloads(ctx);
  }

  /* ------------------------------------------------------------------ *
   * Lock cards & unlocking
   * ------------------------------------------------------------------ */
  var LOCK_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="2"/>' +
    '<path d="M8 11V8a4 4 0 0 1 8 0v3"/><path d="M12 15v2"/></svg>';

  function renderLock(box) {
    if (box.getAttribute('data-rb-init')) return;
    box.setAttribute('data-rb-init', '1');
    var gid = box.getAttribute('data-group');
    var g = groupById[gid] || { id: gid, label: gid };
    var card = el('div', 'rb-lock-card');
    var icon = el('div', 'rb-lock-icon');
    icon.innerHTML = LOCK_SVG;
    card.appendChild(icon);
    card.appendChild(el('h2', 'rb-lock-title', (g.label || gid) + ' · 尚未解鎖'));
    var metaTxt = (g.minute != null && g.minute !== '' ? '到第 ' + g.minute + ' 分鐘時，' : '') + '主持人會公布解鎖碼，輸入後就能看到這一段';
    card.appendChild(el('p', 'rb-lock-meta', metaTxt));
    var form = el('form', 'rb-lock-form');
    form.setAttribute('autocomplete', 'off');
    form.setAttribute('novalidate', '');
    var input = el('input', 'rb-lock-input');
    input.type = 'text';
    input.placeholder = '輸入解鎖碼（不分大小寫）';
    input.setAttribute('aria-label', (g.label || gid) + ' 解鎖碼');
    input.setAttribute('autocomplete', 'off');
    input.setAttribute('autocapitalize', 'characters');
    input.spellcheck = false;
    var btn = el('button', 'rb-lock-btn', '解鎖');
    btn.type = 'submit';
    form.appendChild(input);
    form.appendChild(btn);
    card.appendChild(form);
    var err = el('p', 'rb-lock-error');
    err.setAttribute('role', 'alert');
    err.hidden = true;
    card.appendChild(err);
    function fail(msg) {
      err.textContent = msg;
      err.hidden = false;
      card.classList.remove('is-shake');
      card.classList.add('is-error');
      form.classList.add('is-error');
      void card.offsetWidth;            // restart the animation
      card.classList.add('is-shake');
      setTimeout(function () { card.classList.remove('is-shake'); }, 650);
      try { input.focus(); input.select(); } catch (e) { /* ignore */ }
    }
    on(form, 'submit', function (ev) {
      ev.preventDefault();
      if (!normalizeCode(input.value)) { fail('請輸入解鎖碼。'); return; }
      btn.disabled = true;
      btn.classList.add('is-busy');
      unlock(gid, input.value).then(function (ok) {
        btn.disabled = false;
        btn.classList.remove('is-busy');
        if (!ok) { fail('解鎖碼不正確，請確認後再試一次。'); return; }
        try { $('#rb-main').focus({ preventScroll: true }); } catch (e) { /* ignore */ }   // the form is gone; keep keyboard focus on the page
      });
    });
    on(input, 'input', function () { err.hidden = true; card.classList.remove('is-error'); form.classList.remove('is-error'); });
    box.appendChild(card);
  }

  function applyGroup(gid, content) {
    var g = groupById[gid];
    var pages = (content && content.pages) || {};
    Object.keys((content && content.downloads) || {}).forEach(function (k) { downloadData[k] = content.downloads[k]; });
    Object.keys(pages).forEach(function (pid) {
      var art = articles[pid];
      if (!art) return;
      var body = art.querySelector('.rb-page-body');
      if (!body) { body = el('div', 'rb-page-body'); art.appendChild(body); }
      body.innerHTML = pages[pid];
      art.classList.add('is-unlocked');
      initComponents(body);
      buildSteps(art);
    });
    unlocked[gid] = true;
    if (g && g.pages) g.pages.forEach(function (pid) { if (articles[pid]) articles[pid].classList.add('is-unlocked'); });
  }

  function tryGroup(gid, code) {
    var g = groupById[gid];
    if (!g) return false;
    var n = normalizeCode(code);
    if (!n || makeVerifier(gid, n) !== String(g.verifier || '').toLowerCase()) return false;
    if (unlocked[gid]) return true;
    var content = decodePayload(gid, n, g.payload);
    applyGroup(gid, content);
    store.set('{{STORAGE_PREFIX}}unlocked:' + gid, n);
    return true;
  }

  function afterUnlockChange() {
    updateProgress();
    buildSearchIndex();
    if (currentId) showPage(currentId);
    updateNavStates();
  }

  function unlock(groupId, code) {
    return new Promise(function (resolve) {
      setTimeout(function () {         // let the UI paint (button disabled) before hashing
        var ok = false;
        try { ok = tryGroup(String(groupId), code); } catch (e) {
          ok = false;
          toast('解碼失敗：' + (e && e.message ? e.message : e), 'danger');
        }
        if (ok) {
          afterUnlockChange();
          var g = groupById[groupId];
          toast('已解鎖 ' + ((g && g.label) || groupId), 'unlock');
        }
        resolve(ok);
      }, 0);
    });
  }

  function restoreUnlocked() {
    var restored = [];
    DATA.groups.forEach(function (g) {
      var n = store.get('{{STORAGE_PREFIX}}unlocked:' + g.id);
      if (!n) return;
      try {
        if (tryGroup(g.id, n)) restored.push(g.label || g.id);
        else store.del('{{STORAGE_PREFIX}}unlocked:' + g.id);
      } catch (e) { store.del('{{STORAGE_PREFIX}}unlocked:' + g.id); }
    });
    return restored;
  }

  /* ------------------------------------------------------------------ *
   * Search (titles of all pages + text of open / unlocked pages)
   * ------------------------------------------------------------------ */
  var searchInput = $('.rb-search-input'), searchBox = $('.rb-search-results');
  var index = [], activeHit = -1;

  function buildSearchIndex() {
    index = order.map(function (id) {
      var p = pageById[id] || {};
      var locked = isPageLocked(id);
      var body = articles[id] && articles[id].querySelector('.rb-page-body');
      var text = '';
      if (!locked && body) {
        var clone = body.cloneNode(true);
        $$('script, .rb-copy, .rb-form-card, .rb-zip-warning', clone).forEach(function (n) { n.parentNode.removeChild(n); });
        text = (clone.textContent || '').replace(/\s+/g, ' ').trim();
      }
      return { id: id, title: pageTitle(id), section: p.section || '', locked: locked, text: text,
        hay: (pageTitle(id) + ' ' + (p.section || '')).toLowerCase(), low: text.toLowerCase() };
    });
  }

  function snippet(text, low, q) {
    var i = low.indexOf(q);
    if (i < 0) return '';
    var s = Math.max(0, i - 24), e = Math.min(text.length, i + q.length + 48);
    return (s > 0 ? '…' : '') + text.slice(s, e) + (e < text.length ? '…' : '');
  }

  function closeSearch() {
    if (searchBox) { searchBox.hidden = true; searchBox.innerHTML = ''; }
    activeHit = -1;
  }

  function runSearch() {
    if (!searchInput || !searchBox) return;
    var q = searchInput.value.trim().toLowerCase();
    searchBox.innerHTML = '';
    activeHit = -1;
    if (!q) { searchBox.hidden = true; return; }
    var hits = [];
    index.forEach(function (it) {
      var inTitle = it.hay.indexOf(q) >= 0, inText = it.low.indexOf(q) >= 0;
      if (inTitle || inText) hits.push({ it: it, score: inTitle ? 0 : 1 });
    });
    hits.sort(function (a, b) { return a.score - b.score; });
    hits.slice(0, 12).forEach(function (h) {
      var a = el('a', 'rb-search-hit rb-search-result' + (h.it.locked ? ' is-locked' : ''));
      a.href = '#p-' + h.it.id;
      if (!h.it.locked && steps[h.it.id]) {
        steps[h.it.id].some(function (s) {
          if ((s.el.textContent || '').toLowerCase().indexOf(q) < 0) return false;
          a.href = '#' + s.id;
          return true;
        });
      }
      a.setAttribute('role', 'option');
      a.appendChild(el('b', 'rb-search-result-title', h.it.title));
      if (h.it.section) a.appendChild(el('span', 'rb-search-result-section', h.it.section));
      var sub = h.it.locked ? '尚未解鎖' : snippet(h.it.text, h.it.low, q);
      if (sub) {
        var sn = el('span', 'rb-search-result-snippet');
        var k = h.it.locked ? -1 : sub.toLowerCase().indexOf(q);
        if (k >= 0) {
          sn.appendChild(doc.createTextNode(sub.slice(0, k)));
          sn.appendChild(el('mark', null, sub.slice(k, k + q.length)));
          sn.appendChild(doc.createTextNode(sub.slice(k + q.length)));
        } else sn.textContent = sub;
        a.appendChild(sn);
      }
      on(a, 'mousedown', function (ev) { ev.preventDefault(); });   // keep focus until click resolves
      on(a, 'click', function () {
        closeSearch(); searchInput.value = ''; searchInput.blur();
        setTimeout(function () { revealSearchHit(q); }, 60);
      });
      searchBox.appendChild(a);
    });
    if (!hits.length) {
      var none = el('div', 'rb-search-empty', '找不到「' + searchInput.value.trim() + '」');
      searchBox.appendChild(none);
    }
    searchBox.hidden = false;
  }

  function moveHit(delta) {
    var hits = $$('.rb-search-hit', searchBox);
    if (!hits.length) return;
    activeHit = (activeHit + delta + hits.length) % hits.length;
    hits.forEach(function (h, i) { h.classList.toggle('is-active', i === activeHit); });
    try { hits[activeHit].scrollIntoView({ block: 'nearest' }); } catch (e) { /* ignore */ }
  }

  function initSearch() {
    if (!searchInput) return;
    on(searchInput, 'input', runSearch);
    on(searchInput, 'focus', function () { if (searchInput.value.trim()) runSearch(); });
    on(searchInput, 'blur', function () { setTimeout(closeSearch, 150); });
    on(searchInput, 'keydown', function (ev) {
      if (ev.key === 'ArrowDown') { ev.preventDefault(); moveHit(1); }
      else if (ev.key === 'ArrowUp') { ev.preventDefault(); moveHit(-1); }
      else if (ev.key === 'Enter') {
        ev.preventDefault();
        var hits = $$('.rb-search-hit', searchBox);
        var pick = hits[activeHit >= 0 ? activeHit : 0];
        if (pick) { location.hash = pick.getAttribute('href'); closeSearch(); searchInput.value = ''; searchInput.blur(); }
      } else if (ev.key === 'Escape') { closeSearch(); searchInput.blur(); }
    });
  }

  /* ------------------------------------------------------------------ *
   * Shell chrome: theme, sidebar (mobile), keyboard, zip/temp warning
   * ------------------------------------------------------------------ */
  function initExportBtn() { on($('.rb-export-btn'), 'click', exportAll); }

  function initTheme() {
    on($('.rb-theme-btn'), 'click', function () {
      var t = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', t);
      store.set('{{STORAGE_PREFIX}}theme', t);
    });
  }

  var sidebar = $('.rb-sidebar'), scrim = $('.rb-scrim'), menuBtn = $('.rb-menu-btn');
  function openSidebar() {
    if (!sidebar) return;
    sidebar.classList.add('is-open');
    doc.body.classList.add('is-nav-open');
    if (scrim) scrim.hidden = false;
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'true');
    var cur = $('.rb-nav-link.is-current', sidebar) || $('.rb-nav-link', sidebar);
    if (cur) cur.focus();             // keyboard lands in the menu, scrolled to where you are
  }
  function closeSidebar() {
    if (!sidebar) return;
    sidebar.classList.remove('is-open');
    doc.body.classList.remove('is-nav-open');
    if (scrim) scrim.hidden = true;
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
  }
  function initSidebar() {
    on(menuBtn, 'click', function () { if (sidebar && sidebar.classList.contains('is-open')) closeSidebar(); else openSidebar(); });
    on(scrim, 'click', closeSidebar);
    $$('[data-home]').forEach(function (a) {
      on(a, 'click', function (ev) { ev.preventDefault(); if (order[0]) location.hash = '#p-' + order[0]; });
    });
  }

  function initKeys() {
    on(doc, 'keydown', function (ev) {
      var t = ev.target, tag = t && t.tagName;
      var typing = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (t && t.isContentEditable);
      if (ev.key === 'Escape') {
        var wasOpen = sidebar && sidebar.classList.contains('is-open');
        closeSidebar(); closeSearch();
        if (wasOpen && menuBtn) menuBtn.focus();
        return;
      }
      if (typing || ev.ctrlKey || ev.metaKey || ev.altKey) return;
      if (ev.key === '/' && searchInput) { ev.preventDefault(); searchInput.focus(); searchInput.select(); }
      else if ((ev.key === '[' || ev.key === ']') && currentId) {
        var i = order.indexOf(currentId) + (ev.key === ']' ? 1 : -1);
        if (i >= 0 && i < order.length) location.hash = '#p-' + order[i];
      }
    });
  }

  function zipTempWarning() {
    if (location.protocol !== 'file:') return;
    var href = location.href, dec = href;
    try { dec = decodeURIComponent(href); } catch (e) { dec = href; }
    var re = /\\Temp\\|\/Temp\/|\.zip/i;
    if (!re.test(href) && !re.test(dec)) return;
    var first = order[0] && articles[order[0]] && articles[order[0]].querySelector('.rb-page-body');
    if (!first || first.querySelector('.rb-zip-warning')) return;
    var box = el('div', 'rb-callout rb-callout-warning rb-zip-warning');
    box.appendChild(el('div', 'rb-callout-title', '你可能正從壓縮檔或暫存資料夾開啟 Runbook'));
    var body = el('div', 'rb-callout-body');
    body.appendChild(el('p', null, '請先把整個工作坊資料夾「全部解壓縮」到桌面或文件夾，再從解壓後的資料夾開啟 runbook.html。' +
      '從 ZIP 預覽或暫存資料夾開啟時，表單、勾選進度與解鎖狀態可能在關閉後遺失，下載的檔案也可能找不到。'));
    box.appendChild(body);
    first.insertBefore(box, first.firstChild);
  }

  /* ------------------------------------------------------------------ *
   * Boot
   * ------------------------------------------------------------------ */
  function boot() {
    $$('.rb-lock[data-group]').forEach(renderLock);
    var restored = [];
    try { restored = restoreUnlocked(); } catch (e) { restored = []; }
    zipTempWarning();
    initComponents(doc);
    Object.keys(articles).forEach(function (k) { buildSteps(articles[k]); });
    initSearch();
    initFolds();
    initTheme();
    initExportBtn();
    initSidebar();
    initKeys();
    buildSearchIndex();
    on(window, 'hashchange', route);
    route();
    on(window, 'load', function () { if (/^#p-/.test(location.hash || '') || !location.hash) resetScroll(); });
    updateProgress();
    if (restored.length) toast('已解鎖 ' + restored.join('、'), 'unlock');
    if (!store.ok) toast('瀏覽器封鎖本機儲存：表單與進度不會被保存', 'warning');
    root.classList.add('rb-ready');
  }

  window.RB = {
    version: VERSION,
    unlock: unlock,
    // diagnostics (used by self-tests; harmless for participants)
    _sha256Hex: sha256Hex,
    _normalize: normalizeCode
  };

  try { boot(); } catch (e) {
    if (window.console && console.error) console.error('[runbook] boot failed', e);
    // Last resort: show the first page so content is never blank.
    var firstArt = doc.querySelector('.rb-page');
    if (firstArt) firstArt.hidden = false;
  }
})();
