/* 10-deck-core.js - deck core runtime.
 * Owns: slide collection, stage scaling, slide/fragment states, keyboard
 * (except T/R/P, which belong to 20-deck-features.js), overview, help, black,
 * fullscreen, hash deep link, PLAN/segOf/stageOf, agenda/counter/stage chrome,
 * and the window.DK API + events. Plain ES2018, no libs, works on file://.
 */
(function () {
  "use strict";
  if (window.DK) { return; }

  var STAGE_W = 1920;
  var STAGE_H = 1080;
  var THUMB_W = 288;

  var PLAN = [
    { seg: "dlc-opening", label: "開場", start: 0, end: 10 },
    { seg: "dlc-d1", label: "D1 語言與邊界", start: 10, end: 35 },
    { seg: "dlc-d2", label: "D2 審查核准", start: 35, end: 60 },
    { seg: "dlc-break", label: "休息", start: 60, end: 70 },
    { seg: "dlc-d3a", label: "D3a 電子發票", start: 70, end: 95 },
    { seg: "dlc-d3b", label: "D3b 點數折抵", start: 95, end: 125 },
    { seg: "dlc-d3c", label: "D3c 部分退款", start: 125, end: 155 },
    { seg: "dlc-d4", label: "D4 交接", start: 155, end: 165 },
    { seg: "dlc-retro", label: "回顧", start: 165, end: 180 }
  ];

  // DLC reuses the three stage colours: tool = 開場, teammate = 建立 Domain Memory, dw = 用它驅動變更.
  var STAGE_OF = {
    "dlc-opening": "tool",
    "dlc-d1": "teammate", "dlc-d2": "teammate",
    "dlc-break": "all",
    "dlc-d3a": "dw", "dlc-d3b": "dw", "dlc-d3c": "dw", "dlc-d4": "dw",
    "dlc-retro": "all"
  };

  var STAGE_TEXT = {
    tool: "開場",
    teammate: "建立 Domain Memory",
    dw: "用 Domain Memory 驅動變更",
    all: "Agent 的領域記憶"
  };

  var HELP_KEYS = [
    ["→ / Space / PageDown", "下一步（片段或下一頁）"],
    ["← / PageUp", "上一步"],
    ["Home / End", "第一頁 / 最後一頁"],
    ["O", "總覽（點選縮圖跳頁）"],
    ["F", "全螢幕"],
    ["B", "黑屏"],
    ["T", "開始 / 暫停本段計時（或倒數）"],
    ["R", "重設本段計時"],
    ["P", "開啟主持人視窗"],
    ["?", "顯示 / 隱藏本說明"],
    ["Esc", "關閉覆蓋層"]
  ];

  var isPresenter = (location.hash || "").indexOf("#presenter") === 0;

  /* ---------- helpers ---------- */
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function clamp(n, lo, hi) { return n < lo ? lo : (n > hi ? hi : n); }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) { e.className = cls; }
    if (text != null) { e.textContent = String(text); }
    return e;
  }

  /* ---------- events ---------- */
  var handlers = {};
  function on(evt, fn) {
    if (typeof fn !== "function") { return function () {}; }
    (handlers[evt] = handlers[evt] || []).push(fn);
    return function off() {
      var list = handlers[evt] || [];
      var k = list.indexOf(fn);
      if (k >= 0) { list.splice(k, 1); }
    };
  }
  function emit(evt, data) {
    var list = (handlers[evt] || []).slice();
    for (var k = 0; k < list.length; k++) {
      try { list[k](data); } catch (err) {
        if (window.console && console.error) { console.error("[DK] handler for '" + evt + "' failed:", err); }
      }
    }
    try {
      var ce;
      if (typeof window.CustomEvent === "function") {
        ce = new CustomEvent("dk:" + evt, { detail: data });
      } else {
        ce = document.createEvent("CustomEvent");
        ce.initCustomEvent("dk:" + evt, false, false, data);
      }
      document.dispatchEvent(ce);
    } catch (e2) { /* ignore */ }
  }

  /* ---------- slides & fragments ---------- */
  var viewport = $("#dk-viewport");
  var stage = $("#dk-stage");
  var slides = $all("#dk-stage > section.slide");
  var fragCache = [];
  var index = 0;
  var frag = 0;

  function fragsOf(i) {
    // Only teaching moments explicitly marked for steps consume extra clicks.
    if (slides[i].getAttribute("data-fragments") !== "step") { return []; }
    if (!fragCache[i]) {
      fragCache[i] = $all(".fx", slides[i]).filter(function (f) {
        return !(f.closest && f.closest(".notes"));
      });
    }
    return fragCache[i];
  }

  function segOf(i) {
    if (!slides.length) { return PLAN[0].seg; }
    i = clamp(i | 0, 0, slides.length - 1);
    var k, s;
    for (k = i; k >= 0; k--) {
      s = slides[k].getAttribute("data-seg");
      if (s && s !== "reveal") { return s; }
    }
    for (k = i + 1; k < slides.length; k++) {
      s = slides[k].getAttribute("data-seg");
      if (s && s !== "reveal") { return s; }
    }
    return PLAN[0].seg;
  }

  function stageOf(seg) { return STAGE_OF[seg] || "tool"; }

  function planOf(seg) {
    for (var k = 0; k < PLAN.length; k++) { if (PLAN[k].seg === seg) { return PLAN[k]; } }
    return null;
  }

  function applyFragments(i, n) {
    var list = fragsOf(i);
    for (var k = 0; k < list.length; k++) {
      if (k < n) { list[k].classList.add("is-shown"); } else { list[k].classList.remove("is-shown"); }
    }
  }

  function applySlideStates() {
    for (var k = 0; k < slides.length; k++) {
      var c = slides[k].classList;
      c.toggle("is-active", k === index);
      c.toggle("is-past", k < index);
      c.toggle("is-future", k > index);
      if (k === index) { slides[k].removeAttribute("aria-hidden"); } else { slides[k].setAttribute("aria-hidden", "true"); }
    }
  }

  function changeData() {
    var seg = segOf(index);
    return { index: index, frag: frag, slide: slides[index] || null, seg: seg, stage: stageOf(seg), total: slides.length };
  }

  /* go(i, frag?): frag omitted -> 0; frag < 0 or "all" -> all fragments shown. */
  function go(i, f) {
    if (!slides.length) { return; }
    var target = clamp(parseInt(i, 10) || 0, 0, slides.length - 1);
    var total = fragsOf(target).length;
    var nf;
    if (f === "all" || (typeof f === "number" && f < 0)) { nf = total; }
    else if (f == null || f === "") { nf = 0; }
    else { nf = clamp(parseInt(f, 10) || 0, 0, total); }
    var prevIndex = index;
    index = target;
    frag = nf;
    if (prevIndex !== target && slides[prevIndex]) { applyFragments(prevIndex, prevIndex < target ? fragsOf(prevIndex).length : 0); }
    applySlideStates();
    applyFragments(index, frag);
    updateChrome();
    writeHash();
    if (overviewOpen) { markOverviewCurrent(); }
    emit("change", changeData());
  }

  function next() {
    if (!slides.length) { return; }
    if (frag < fragsOf(index).length) { go(index, frag + 1); }
    else if (index < slides.length - 1) { go(index + 1, 0); }
  }

  function prev() {
    if (!slides.length) { return; }
    if (frag > 0) { go(index, frag - 1); }
    else if (index > 0) { go(index - 1, "all"); }
  }

  /* ---------- stage scaling ---------- */
  function scaleStage() {
    if (!stage) { return; }
    var vw = 0, vh = 0;
    if (viewport) { vw = viewport.clientWidth; vh = viewport.clientHeight; }
    if (!vw || !vh) { vw = window.innerWidth || document.documentElement.clientWidth || STAGE_W; vh = window.innerHeight || document.documentElement.clientHeight || STAGE_H; }
    var s = Math.min(vw / STAGE_W, vh / STAGE_H);
    if (!(s > 0)) { s = 1; }
    var x = (vw - STAGE_W * s) / 2;
    var y = (vh - STAGE_H * s) / 2;
    stage.style.position = "absolute";
    stage.style.left = "0";
    stage.style.top = "0";
    stage.style.width = STAGE_W + "px";
    stage.style.height = STAGE_H + "px";
    stage.style.transformOrigin = "0 0";
    stage.style.transform = "translate(" + x.toFixed(2) + "px," + y.toFixed(2) + "px) scale(" + s.toFixed(5) + ")";
    document.documentElement.style.setProperty("--dk-scale", s.toFixed(5));
  }

  /* ---------- chrome: agenda, counter, stage indicator ---------- */
  var agendaEl = $(".dk-agenda");
  var counterEl = $(".dk-counter");
  var stageIndEl = $(".dk-stage-ind");
  var agendaSegs = [];

  function firstSlideOfSeg(seg) {
    for (var k = 0; k < slides.length; k++) { if (segOf(k) === seg) { return k; } }
    return -1;
  }

  function buildAgenda() {
    if (!agendaEl) { return; }
    agendaEl.innerHTML = "";
    agendaSegs = PLAN.map(function (p) {
      var d = el("div", "dk-agenda-seg");
      d.setAttribute("data-seg", p.seg);
      d.setAttribute("data-stage", stageOf(p.seg));
      d.style.flexGrow = String(p.end - p.start);
      d.title = p.label + " · " + pad2(p.start) + "–" + pad2(p.end);
      d.appendChild(el("span", "dk-agenda-label", p.label));
      d.addEventListener("click", function () {
        var k = firstSlideOfSeg(p.seg);
        if (k >= 0) { go(k, 0); }
      });
      agendaEl.appendChild(d);
      return d;
    });
  }

  function pad2(n) { n = String(n); return n.length < 2 ? "0" + n : n; }

  function updateChrome() {
    var seg = segOf(index);
    var stg = stageOf(seg);
    var curPos = -1;
    for (var k = 0; k < PLAN.length; k++) { if (PLAN[k].seg === seg) { curPos = k; } }
    for (k = 0; k < agendaSegs.length; k++) {
      agendaSegs[k].classList.toggle("is-current", k === curPos);
      agendaSegs[k].classList.toggle("is-past", curPos >= 0 && k < curPos);
    }
    if (counterEl) { counterEl.textContent = (slides.length ? index + 1 : 0) + " / " + slides.length; }
    if (stageIndEl) {
      stageIndEl.textContent = STAGE_TEXT[stg] || "";
      stageIndEl.setAttribute("data-stage", stg);
    }
    if (document.body) {
      document.body.setAttribute("data-seg", seg);
      document.body.setAttribute("data-stage", stg);
    }
  }

  /* ---------- hash deep link: #/<n> (1-based), optional #/<n>.<frag> ---------- */
  function parseHash() {
    var h = location.hash || "";
    if (h.indexOf("#presenter") === 0) { return null; }
    var m = /^#\/(\d+)(?:\.(\d+))?/.exec(h);
    if (!m) { return null; }
    return { index: parseInt(m[1], 10) - 1, frag: m[2] != null ? parseInt(m[2], 10) : null };
  }

  var lastHash = "";
  function writeHash() {
    if (isPresenter) { return; }
    if ((location.hash || "").indexOf("#presenter") === 0) { return; }
    var h = "#/" + (index + 1);
    if (location.hash === h) { lastHash = h; return; }
    lastHash = h;
    try {
      history.replaceState(history.state, "", h);
    } catch (e) {
      try { location.replace(h); } catch (e2) { /* ignore */ }
    }
  }

  function onHashChange() {
    if (isPresenter) { return; }
    var p = parseHash();
    if (!p) { return; }
    if (location.hash === lastHash) { return; }
    var target = clamp(p.index, 0, Math.max(0, slides.length - 1));
    if (target === index && p.frag == null) { return; }
    go(target, p.frag);
  }

  /* ---------- overlays: overview, help, black ---------- */
  var overviewEl = $("#dk-overview");
  var helpEl = $("#dk-help");
  var blackEl = $("#dk-black");
  var overviewOpen = false;
  var overviewBuilt = false;
  var thumbs = [];

  function stripForClone(node) {
    $all(".notes, script", node).forEach(function (n) { if (n.parentNode) { n.parentNode.removeChild(n); } });
    $all("[id]", node).forEach(function (n) { n.removeAttribute("id"); });
    $all(".fx", node).forEach(function (n) { n.classList.add("is-shown"); });
    if (node.removeAttribute) { node.removeAttribute("id"); node.removeAttribute("aria-hidden"); }
    return node;
  }

  function buildOverview() {
    if (!overviewEl || overviewBuilt) { return; }
    overviewBuilt = true;
    var s = THUMB_W / STAGE_W;
    var grid = el("div", "dk-overview-grid");
    thumbs = slides.map(function (slide, k) {
      var t = el("button", "dk-thumb");
      t.type = "button";
      t.setAttribute("data-index", String(k));
      t.setAttribute("data-seg", segOf(k));
      var title = slide.getAttribute("data-title") || "";
      t.setAttribute("data-title", title);
      t.title = (k + 1) + ". " + title;
      var frame = el("div", "dk-thumb-frame");
      frame.style.position = "relative";
      frame.style.overflow = "hidden";
      frame.style.width = THUMB_W + "px";
      frame.style.height = Math.round(STAGE_H * s) + "px";
      var clone = stripForClone(slide.cloneNode(true));
      clone.classList.remove("is-past", "is-future");
      clone.classList.add("is-active", "dk-thumb-slide");
      clone.style.position = "absolute";
      clone.style.left = "0";
      clone.style.top = "0";
      clone.style.width = STAGE_W + "px";
      clone.style.height = STAGE_H + "px";
      clone.style.transformOrigin = "0 0";
      clone.style.transform = "scale(" + s.toFixed(5) + ")";
      clone.style.pointerEvents = "none";
      clone.setAttribute("aria-hidden", "true");
      frame.appendChild(clone);
      t.appendChild(frame);
      var cap = el("div", "dk-thumb-cap");
      cap.appendChild(el("span", "dk-thumb-num", k + 1));
      cap.appendChild(el("span", "dk-thumb-title", title));
      t.appendChild(cap);
      t.addEventListener("click", function () {
        closeOverlays();
        go(k, 0);
      });
      grid.appendChild(t);
      return t;
    });
    overviewEl.appendChild(grid);
  }

  function markOverviewCurrent() {
    for (var k = 0; k < thumbs.length; k++) { thumbs[k].classList.toggle("is-current", k === index); }
    var cur = thumbs[index];
    if (cur && cur.scrollIntoView) {
      try { cur.scrollIntoView({ block: "nearest" }); } catch (e) { cur.scrollIntoView(false); }
    }
  }

  function setOverlay(node, open, bodyClass) {
    if (!node) { return; }
    node.hidden = !open;
    if (document.body) { document.body.classList.toggle(bodyClass, open); }
  }

  function toggleOverview(force) {
    var open = typeof force === "boolean" ? force : !overviewOpen;
    if (open) { buildOverview(); setOverlay(helpEl, false, "dk-help-open"); }
    overviewOpen = open && !!overviewEl;
    setOverlay(overviewEl, overviewOpen, "dk-overview-open");
    if (overviewOpen) { markOverviewCurrent(); }
    emit("overlay", { name: "overview", open: overviewOpen });
  }

  function buildHelp() {
    if (!helpEl || helpEl.getAttribute("data-built")) { return; }
    helpEl.setAttribute("data-built", "1");
    var box = el("div", "dk-help-box");
    box.appendChild(el("h2", "dk-help-title", "鍵盤快捷鍵"));
    var dl = el("dl", "dk-help-keys");
    HELP_KEYS.forEach(function (row) {
      dl.appendChild(el("dt", "", row[0]));
      dl.appendChild(el("dd", "", row[1]));
    });
    box.appendChild(dl);
    box.appendChild(el("p", "dk-help-foot", "網址 #/頁碼 可直接開啟指定頁；按 Esc 或 ? 關閉。"));
    helpEl.appendChild(box);
    helpEl.addEventListener("click", function () { toggleHelp(false); });
  }

  function toggleHelp(force) {
    if (!helpEl) { return; }
    var open = typeof force === "boolean" ? force : helpEl.hidden;
    if (open) { buildHelp(); }
    setOverlay(helpEl, open, "dk-help-open");
    emit("overlay", { name: "help", open: open });
  }

  function toggleBlack(force) {
    if (!blackEl) { return; }
    var open = typeof force === "boolean" ? force : blackEl.hidden;
    setOverlay(blackEl, open, "dk-black-on");
    emit("overlay", { name: "black", open: open });
  }

  function closeOverlays() {
    var any = false;
    if (overviewOpen) { toggleOverview(false); any = true; }
    if (helpEl && !helpEl.hidden) { toggleHelp(false); any = true; }
    if (blackEl && !blackEl.hidden) { toggleBlack(false); any = true; }
    return any;
  }

  /* ---------- fullscreen ---------- */
  function toggleFullscreen() {
    var d = document;
    var de = d.documentElement;
    var fsEl = d.fullscreenElement || d.webkitFullscreenElement;
    var p = null;
    try {
      if (fsEl) {
        p = d.exitFullscreen ? d.exitFullscreen() : (d.webkitExitFullscreen ? d.webkitExitFullscreen() : null);
      } else {
        p = de.requestFullscreen ? de.requestFullscreen() : (de.webkitRequestFullscreen ? de.webkitRequestFullscreen() : null);
      }
    } catch (e) { p = null; }
    if (p && typeof p.catch === "function") { p.catch(function () { /* user-gesture or policy refusal */ }); }
  }

  /* ---------- keyboard (T/R/P intentionally NOT handled here) ---------- */
  function isTypingTarget(t) {
    if (!t || t === document.body) { return false; }
    var tag = (t.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select") { return true; }
    return !!t.isContentEditable;
  }

  function onKeyDown(e) {
    if (e.defaultPrevented) { return; }
    if (e.ctrlKey || e.metaKey || e.altKey) { return; }
    if (isTypingTarget(e.target)) { return; }
    var key = e.key;
    var code = e.code || "";
    var handled = true;

    switch (key) {
      case "ArrowRight":
      case "PageDown":
        next();
        break;
      case " ":
      case "Spacebar":
        if (e.shiftKey) { prev(); } else { next(); }
        break;
      case "ArrowLeft":
      case "PageUp":
        prev();
        break;
      case "Home":
        go(0, 0);
        break;
      case "End":
        go(slides.length - 1, 0);
        break;
      case "Enter":
        if (overviewOpen) { toggleOverview(false); } else { handled = false; }
        break;
      case "Escape":
      case "Esc":
        handled = closeOverlays();
        break;
      case "?":
        if (isPresenter) { handled = false; } else { toggleHelp(); }
        break;
      default:
        handled = false;
    }

    if (!handled && key && key.length === 1) {
      var k = key.toLowerCase();
      if (k === "o" && !isPresenter) { toggleOverview(); handled = true; }
      else if (k === "f") { toggleFullscreen(); handled = true; }
      else if (k === "b" && !isPresenter) { toggleBlack(); handled = true; }
      else if (k === "/" && e.shiftKey && !isPresenter) { toggleHelp(); handled = true; }
      /* t / r / p: left to 20-deck-features.js - no preventDefault here. */
    } else if (!handled && code === "Slash" && e.shiftKey && !isPresenter) {
      toggleHelp(); handled = true;
    }

    if (handled) { e.preventDefault(); }
  }

  /* ---------- public API ---------- */
  var DK = {
    slides: slides,
    PLAN: PLAN,
    get index() { return index; },
    get frag() { return frag; },
    get total() { return slides.length; },
    go: go,
    next: next,
    prev: prev,
    segOf: segOf,
    stageOf: stageOf,
    planOf: planOf,
    fragCount: function (i) { return slides[i] ? fragsOf(i).length : 0; },
    on: on,
    emit: emit,
    isPresenter: isPresenter,
    ready: false,
    overview: toggleOverview,
    help: toggleHelp,
    black: toggleBlack,
    fullscreen: toggleFullscreen,
    closeOverlays: closeOverlays,
    rescale: function () { scaleStage(); }
  };
  window.DK = DK;

  /* ---------- init ---------- */
  function init() {
    if (document.body) {
      document.body.classList.toggle("is-presenter", isPresenter);
    }
    buildAgenda();
    var p = parseHash();
    var startIndex = p ? clamp(p.index, 0, Math.max(0, slides.length - 1)) : 0;
    var startFrag = p && p.frag != null ? clamp(p.frag, 0, slides.length ? fragsOf(startIndex).length : 0) : 0;
    index = startIndex;
    frag = startFrag;
    for (var k = 0; k < slides.length; k++) {
      applyFragments(k, k < index ? fragsOf(k).length : (k === index ? frag : 0));
    }
    applySlideStates();
    updateChrome();
    scaleStage();
    if (slides.length) { writeHash(); }

    window.addEventListener("resize", scaleStage);
    window.addEventListener("orientationchange", scaleStage);
    document.addEventListener("fullscreenchange", scaleStage);
    document.addEventListener("webkitfullscreenchange", scaleStage);
    window.addEventListener("hashchange", onHashChange);
    document.addEventListener("keydown", onKeyDown);
    if (blackEl) { blackEl.addEventListener("click", function () { toggleBlack(false); }); }

    /* Initial 'change' fires after every DOMContentLoaded listener (features) has registered. */
    function fireInitial() {
      setTimeout(function () {
        DK.ready = true;
        scaleStage();
        emit("ready", changeData());
        emit("change", changeData());
      }, 0);
    }
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fireInitial);
    } else {
      fireInitial();
    }
  }

  try {
    init();
  } catch (err) {
    if (window.console && console.error) { console.error("[DK] core init failed:", err); }
  }
})();
