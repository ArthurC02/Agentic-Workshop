"""Build the facilitator deck and the participant runbook single-file HTML materials.

Usage:
    python -X utf8 scripts/build_materials.py [--check] [--only deck|runbook]

Inputs live under agentic-workshop/materials/. Participant text is read in-memory from the
hash-verified participant ZIPs of the controlled candidate dist/p11-candidate/<CANDIDATE_ID>/.
The build never calls build_delivery.build() or repin_reviewed_sources(); it only imports pure helpers.
--check rebuilds in memory and exits 1 when the files on disk differ.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import io
import json
import os
import re
import sys
import zipfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import build_delivery  # noqa: E402  (pure helpers only; never build()/repin)

MATERIALS = ROOT / "agentic-workshop" / "materials"
CANDIDATE_ID = "524731ecda74e827"
CANDIDATE = ROOT / "dist" / "p11-candidate" / CANDIDATE_ID

SEGMENTS = ("opening", "greenfield", "timeskip", "analysis", "shared", "b1", "b2", "b3",
            "delivery", "retro", "reveal")
# (segment, start minute, end minute, label) -- component spec B2.
PLAN = (("opening", 0, 7, "開場"), ("greenfield", 7, 29, "Greenfield"), ("timeskip", 29, 33, "Time Skip"),
        ("analysis", 33, 39, "個人分析"), ("shared", 39, 44, "Shared Context"), ("b1", 44, 52, "B1"),
        ("b2", 52, 63, "B2"), ("b3", 63, 76, "B3"), ("delivery", 76, 80, "交付"), ("retro", 80, 90, "回顧"))
FORBIDDEN_MARKERS = ("facilitator", "evaluation", "reference-solution", "reference answer", "標準答案",
                     "STUDENT_FARE_RATE", "intentional failure manifest")
# Same expressions as build_delivery.content_policy (B0 pedagogy guard), applied to rendered pages
# that are visible before the corresponding reveal.
B0_DIAGNOSIS = re.compile(r"受控.{0,12}(?:學生|student).{0,12}(?:Bug|錯|缺陷)|(?:學生|student).{0,12}(?:Bug|85%|錯誤率)|BUG-B0-001", re.I)
B0_PRIORITY = re.compile(r"企業.{0,20}提前.{0,20}學生|CORP(?:ORATE)?.{0,20}ADV(?:ANCE)?.{0,20}STUDENT", re.I)
URL_RE = re.compile(r"https?://[^\s\"'<>)\]]*", re.I)
LOCAL_URL_RE = re.compile(r"https?://(?:127\.0\.0\.1|localhost)(?=[:/]|$)", re.I)
# XML namespace identifiers are not network requests (e.g. createElementNS in JS).
NAMESPACE_URLS = ("http://www.w3.org/2000/svg", "http://www.w3.org/1999/xhtml", "http://www.w3.org/1999/xlink")
WINDOW = 30
RECOVERY_DOWNLOADS = {"recovery-52-b1.zip": ("recovery-b1", 52),
                      "recovery-63-b2.zip": ("recovery-b2", 63)}
RECOVERY_GROUPS = {group: minute for group, minute in RECOVERY_DOWNLOADS.values()}
# Reviewed exemptions for forbidden markers: (page id, exact phrase that contains the marker).
# Only a hit lying fully inside the phrase on that page is tolerated; it is still printed every build.
# - b3-exception-card: frozen candidate text (participant-63-b3-governance,
#   04-digital-worker/participant/06-exception-response-card.md) that states the blank card does NOT
#   pre-release the scenario or the answer. Remove this entry to make the build strict again.
MARKER_EXEMPTIONS = (("b3-exception-card", "空白範本不預發情境或標準答案"),)
TOTAL_MINUTES = 90
STORAGE_PREFIX_TOKEN = "{{STORAGE_PREFIX}}"


@dataclass(frozen=True)
class Edition:
    """One course edition: where its sources live and the rules its materials are validated against."""
    name: str
    materials: Path
    candidate_id: str
    candidate_root: Path
    plan: tuple
    total_minutes: int
    recovery_downloads: dict = field(default_factory=dict)
    marker_exemptions: tuple = ()
    forbidden_markers: tuple = FORBIDDEN_MARKERS
    b0_guard: bool = False  # B0 pedagogy regexes + build_delivery.content_policy (main course only)
    storage_prefix: str = "stw:"  # runbook localStorage key prefix; file:// pages share one origin
    package_output: str = "dist/materials/participant-materials.zip"  # relative to ROOT

    def __post_init__(self):
        if not re.fullmatch(r"[a-z0-9]+:", self.storage_prefix):
            raise BuildError("storage_prefix must match [a-z0-9]+:", [self.storage_prefix])

    @property
    def candidate_dir(self) -> Path:
        return self.candidate_root / self.candidate_id

    @property
    def segments(self) -> tuple:
        return tuple(seg for seg, *_rest in self.plan) + ("reveal",)

    @property
    def recovery_groups(self) -> dict:
        return {group: minute for group, minute in self.recovery_downloads.values()}


DLC_MATERIALS = ROOT / "agentic-workshop" / "materials-dlc"


def load_edition(name: str = "main") -> Edition:
    if name == "main":
        return MAIN
    if name != "dlc":
        raise BuildError("Unknown edition", [name])
    # ponytail: DLC declares plan/candidate/recovery downloads in its own edition.json.
    path = DLC_MATERIALS / "edition.json"
    if not path.exists():
        raise BuildError("DLC edition is not set up yet", [
            f"missing {path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path}",
            'expected JSON: {"candidate_id": "<hash16 under dist/dlc-candidate/>", "total_minutes": 180, '
            '"plan": [["opening", 0, 10, "開場"], ...], "marker_exemptions": [["page-id", "exact phrase"]]}'])
    try:
        cfg = json.loads(read_text(path))
        return Edition(name="dlc", materials=DLC_MATERIALS, candidate_id=str(cfg["candidate_id"]),
                       candidate_root=ROOT / "dist" / "dlc-candidate",
                       plan=tuple((str(s), int(a), int(b), str(label)) for s, a, b, label in cfg["plan"]),
                       total_minutes=int(cfg["total_minutes"]),
                       recovery_downloads={str(name): (str(group), int(minute)) for name, (group, minute)
                                           in cfg.get("recovery_downloads", {}).items()},
                       marker_exemptions=tuple(tuple(x) for x in cfg.get("marker_exemptions", ())),
                       forbidden_markers=tuple(cfg.get("forbidden_markers", FORBIDDEN_MARKERS)),
                       storage_prefix="stwdlc:",
                       package_output="dist/materials-dlc/participant-materials-dlc.zip")
    except (KeyError, TypeError, ValueError) as exc:
        raise BuildError("Invalid DLC edition.json", [f"{path}: {type(exc).__name__}: {exc}"]) from exc


class BuildError(Exception):
    """A build or safety failure. ``problems`` lists every individual message."""

    def __init__(self, title: str, problems: list[str] | None = None):
        self.problems = list(problems or [])
        super().__init__(title + ("".join("\n  - " + p for p in self.problems)))


MAIN = Edition(name="main", materials=MATERIALS, candidate_id=CANDIDATE_ID, candidate_root=CANDIDATE.parent,
               plan=PLAN, total_minutes=TOTAL_MINUTES, recovery_downloads=RECOVERY_DOWNLOADS,
               marker_exemptions=MARKER_EXEMPTIONS, b0_guard=True)


# ---------------------------------------------------------------- generic helpers

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def long_path(path: Path) -> str:
    """Return a path string usable on Windows even beyond MAX_PATH."""
    text = str(Path(path).resolve())
    if os.name == "nt" and not text.startswith("\\\\?\\") and len(text) > 240:
        text = "\\\\?\\" + text
    return text


def read_bytes(path: Path) -> bytes:
    with open(long_path(path), "rb") as handle:
        return handle.read()


def read_text(path: Path) -> str:
    return read_bytes(path).decode("utf-8")


def inputs_digest(items: list[tuple[str, bytes]]) -> str:
    h = hashlib.sha256()
    for name, data in sorted(items, key=lambda x: x[0]):
        h.update(name.encode("utf-8") + b"\0" + str(len(data)).encode() + b"\0" + data)
    return h.hexdigest()


def fill_template(template: str, values: dict[str, str]) -> str:
    """Single-pass placeholder substitution; inserted content is never re-scanned."""
    missing = [k for k in values if "{{" + k + "}}" not in template]
    if missing:
        raise BuildError("Template lacks placeholders", missing)
    out = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: values[m.group(1)] if m.group(1) in values else m.group(0), template)
    leftover = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", template)) - {"{{" + k + "}}" for k in values})
    if leftover:
        raise BuildError("Template has unfilled placeholders", leftover)
    return out


def script_safe_json(value) -> str:
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
    # '<' only occurs inside JSON strings, so < keeps the JSON valid and the script element closed.
    return text.replace("<", "\\u003c")


def load_codes(materials: Path, recovery_groups: dict = RECOVERY_GROUPS) -> list[dict]:
    data = json.loads(read_text(materials / "unlock-codes.json"))
    groups = data.get("groups")
    problems = []
    if not isinstance(groups, list) or not groups:
        raise BuildError("unlock-codes.json must contain a non-empty 'groups' list")
    seen = set()
    for g in groups:
        for key in ("id", "minute", "code", "label"):
            if key not in g or g[key] in ("", None):
                problems.append(f"group {g.get('id')!r} lacks {key}")
        if g.get("id") in seen:
            problems.append(f"duplicate group id {g.get('id')!r}")
        seen.add(g.get("id"))
        if g.get("id") in recovery_groups and g.get("minute") != recovery_groups[g["id"]]:
            problems.append(f"recovery group {g['id']!r} has incorrect release minute")
        if g.get("id") == "open":
            problems.append("'open' is reserved and cannot be an unlock group")
        if g.get("code") is not None and len(normalize_code(str(g["code"]))) < 4:
            problems.append(f"group {g.get('id')!r} code too short after normalization")
    if problems:
        raise BuildError("Invalid unlock-codes.json", problems)
    for g in groups:
        if g["id"] in recovery_groups and any(
                other["id"] != g["id"] and normalize_code(str(other["code"])) == normalize_code(str(g["code"]))
                for other in groups):
            raise BuildError("Recovery unlock code must be independent", [g["id"]])
    return groups


# ---------------------------------------------------------------- scheme B (A5)

def normalize_code(code: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", code.upper())


def verifier(group_id: str, code: str) -> str:
    return sha256_hex(("verify:" + group_id + ":" + normalize_code(code)).encode("utf-8"))


def keystream(group_id: str, code: str, length: int) -> bytes:
    n = normalize_code(code)
    blocks = []
    total = 0
    i = 0
    while total < length:
        block = hashlib.sha256(("ks:" + group_id + ":" + n + ":" + str(i)).encode("utf-8")).digest()
        blocks.append(block)
        total += len(block)
        i += 1
    return b"".join(blocks)[:length]


def xor_bytes(data: bytes, key: bytes) -> bytes:
    if not data:
        return b""
    return (int.from_bytes(data, "big") ^ int.from_bytes(key[:len(data)], "big")).to_bytes(len(data), "big")


def encode_payload(group_id: str, code: str, obj: dict) -> str:
    raw = json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return base64.b64encode(xor_bytes(raw, keystream(group_id, code, len(raw)))).decode("ascii")


def decode_payload(group_id: str, code: str, payload: str, expected_verifier: str | None = None) -> dict:
    if expected_verifier is not None and verifier(group_id, code) != expected_verifier:
        raise ValueError("unlock code does not match verifier")
    raw = base64.b64decode(payload)
    return json.loads(xor_bytes(raw, keystream(group_id, code, len(raw))).decode("utf-8"))


# ---------------------------------------------------------------- text + safety scans

class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag in ("p", "div", "li", "tr", "td", "th", "br", "h2", "h3", "h4", "h5", "h6", "pre", "section"):
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        elif tag in ("p", "div", "li", "tr", "td", "th", "h2", "h3", "h4", "h5", "h6", "pre", "section"):
            self.parts.append(" ")

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def visible_text(markup: str) -> str:
    parser = _TextExtractor()
    parser.feed(markup)
    parser.close()
    return re.sub(r"\s+", " ", "".join(parser.parts)).strip()


def check_codes(document: str, groups: list[dict]) -> list[str]:
    """Unlock codes must never appear in the participant HTML, raw or normalized (case-insensitive)."""
    upper = document.upper()
    problems = []
    for g in groups:
        raw = str(g["code"]).upper()
        norm = normalize_code(str(g["code"]))
        for form in sorted({raw, norm}):
            if form and form in upper:
                problems.append(f"unlock code for group {g['id']!r} appears in output ({form})")
    return problems


def check_plaintext_windows(document: str, locked_html: dict[str, str], open_text: str,
                            width: int = WINDOW, stride: int = 10, strip: tuple[str, ...] = ()) -> list[str]:
    """No 30-char window of a locked page's visible text may appear in the output.

    Windows that also occur in open (public) text are legitimate shared phrasing and are skipped.
    The output is searched raw, entity-decoded, whitespace-collapsed and as extracted visible text so
    tag boundaries cannot hide a leak. ``strip`` removes opaque blobs (encoded payloads) first.
    """
    for blob in strip:
        if blob:
            document = document.replace(blob, "")
    unescaped = html.unescape(document)
    haystacks = (document, unescaped, re.sub(r"\s+", " ", unescaped), visible_text(document))
    seen: set[str] = set()
    for hay in haystacks:
        seen.update(hay[i:i + width] for i in range(0, max(0, len(hay) - width + 1)))
    problems = []
    for page_id, markup in locked_html.items():
        text = visible_text(markup)
        if len(text) < width:
            starts = [0] if text else []
        else:
            starts = list(range(0, len(text) - width + 1, stride))
            if starts[-1] != len(text) - width:
                starts.append(len(text) - width)
        for start in starts:
            window = text[start:start + width]
            if len(window.strip()) < min(width, 12) or window in open_text:
                continue
            if window in seen or (len(window) < width and any(window in h for h in haystacks)):
                problems.append(f"locked page {page_id!r} plaintext visible in output: {window!r}")
                break
    return problems


def _exempt(page_id: str, low: str, pos: int, length: int, exemptions) -> str | None:
    for ex_page, phrase in exemptions:
        if ex_page != page_id:
            continue
        p = phrase.lower()
        start = low.find(p)
        while start >= 0:
            if start <= pos and pos + length <= start + len(p):
                return phrase
            start = low.find(p, start + 1)
    return None


def scan_forbidden(texts: dict[str, str], markers=FORBIDDEN_MARKERS, exemptions=(),
                   exempted: list[str] | None = None) -> list[str]:
    """Case-insensitive marker scan. A hit fully inside a reviewed (page id, exact phrase) exemption is
    moved to ``exempted`` instead of failing; every other occurrence is returned as a hit."""
    hits = []
    for page_id, text in texts.items():
        low = text.lower()
        for marker in markers:
            m = marker.lower()
            pos = low.find(m)
            while pos >= 0:
                context = re.sub(r"\s+", " ", text[max(0, pos - 30):pos + len(m) + 30])
                message = f"[{page_id}] forbidden marker {marker!r}: …{context}…"
                phrase = _exempt(page_id, low, pos, len(m), exemptions)
                if phrase is None:
                    hits.append(message)
                elif exempted is not None:
                    exempted.append(message + f" (reviewed exemption: {phrase!r})")
                pos = low.find(m, pos + 1)
    return hits


def scan_urls(texts: dict[str, str], allow_namespaces: bool = False) -> list[str]:
    hits = []
    for page_id, text in texts.items():
        for m in URL_RE.finditer(text):
            url = m.group(0)
            if LOCAL_URL_RE.match(url):
                continue
            if allow_namespaces and url.rstrip("/") in NAMESPACE_URLS:
                continue
            hits.append(f"[{page_id}] external URL: {url}")
    return hits


def scan_b0_policy(pages: list[dict], texts: dict[str, str], group_minutes: dict[str, int]) -> list[str]:
    """Pages visible before B1 (44) must not disclose the B0 diagnosis; before B2 (52) not the priority."""
    b1 = group_minutes.get("b1", 44)
    b2 = group_minutes.get("b2", 52)
    hits = []
    for page in pages:
        minute = 0 if page["group"] == "open" else group_minutes.get(page["group"], 0)
        text = visible_text(texts.get(page["id"], ""))
        if minute < b1:
            for m in B0_DIAGNOSIS.finditer(text):
                hits.append(f"[{page['id']}] B0 diagnosis disclosed before B1: {m.group(0)!r}")
        if minute < b2:
            for m in B0_PRIORITY.finditer(text):
                hits.append(f"[{page['id']}] discount priority disclosed before B2: {m.group(0)!r}")
    return hits


# ---------------------------------------------------------------- deck (B)

class _SlideParser(HTMLParser):
    """Collect top-level <section class="slide"> elements with their notes presence."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.slides: list[dict] = []
        self._depth = 0
        self._current: dict | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section":
            classes = (a.get("class") or "").split()
            if self._depth == 0 and "slide" in classes:
                self._current = {"attrs": a, "notes": False, "line": self.getpos()[0]}
                self.slides.append(self._current)
            self._depth += 1
        elif tag == "aside" and self._current is not None:
            if "notes" in (a.get("class") or "").split():
                self._current["notes"] = True

    def handle_endtag(self, tag):
        if tag == "section" and self._depth:
            self._depth -= 1
            if self._depth == 0:
                self._current = None


def plan_problems(plan=PLAN, total: int = TOTAL_MINUTES) -> list[str]:
    problems = []
    expected = 0
    for seg, start, end, _label in plan:
        if start != expected:
            problems.append(f"plan segment {seg} starts at {start}, expected {expected} (gap/overlap)")
        if end <= start:
            problems.append(f"plan segment {seg} has non-positive length")
        expected = end
    if plan and plan[0][1] != 0:
        problems.append("plan must start at minute 0")
    if sum(end - start for _, start, end, _ in plan) != total or expected != total:
        problems.append(f"plan segments must total {total} minutes ending at {total}")
    return problems


def validate_slides(slides_html: str, groups: list[dict], plan=None, edition: Edition = MAIN) -> list[dict]:
    """Validate deck slides; returns parsed slides or raises BuildError listing every problem."""
    plan = edition.plan if plan is None else plan
    segments = tuple(seg for seg, *_rest in plan) + ("reveal",)
    recovery_groups = edition.recovery_groups
    if isinstance(slides_html, str):
        parser = _SlideParser()
        parser.feed(slides_html)
        parser.close()
        slides = parser.slides
    else:
        slides = list(slides_html)
    problems = plan_problems(plan, edition.total_minutes)
    group_ids = {g["id"]: g for g in groups}
    plan_index = {seg: i for i, (seg, *_rest) in enumerate(plan)}
    plan_start = {seg: start for seg, start, _e, _l in plan}
    unlocks: dict[str, int] = {}
    last_index = -1
    effective = None
    if not slides:
        problems.append("no <section class=\"slide\"> found")
    for n, s in enumerate(slides, 1):
        a = s["attrs"]
        where = f"slide {n} ({a.get('data-title') or '?'}, {s.get('file', '')}:{s['line']})"
        seg = a.get("data-seg")
        if seg not in segments:
            problems.append(f"{where}: data-seg {seg!r} not in {segments}")
        if not (a.get("data-title") or "").strip():
            problems.append(f"{where}: missing data-title")
        if not s["notes"]:
            problems.append(f"{where}: missing <aside class=\"notes\">")
        if seg == "reveal":
            if not (a.get("data-reveal-of") or "").strip():
                problems.append(f"{where}: reveal slide lacks data-reveal-of")
            if effective is None:
                problems.append(f"{where}: reveal slide cannot precede every segment slide")
        elif seg in plan_index:
            if plan_index[seg] < last_index:
                problems.append(f"{where}: segment {seg} out of plan order")
            last_index = max(last_index, plan_index[seg])
            effective = seg
        if a.get("data-timer") is not None and not re.fullmatch(r"\d{1,2}:\d{2}", a["data-timer"]):
            problems.append(f"{where}: data-timer must be mm:ss")
        if a.get("data-countdown") is not None and not a["data-countdown"].isdigit():
            problems.append(f"{where}: data-countdown must be seconds")
        unlock = a.get("data-unlock")
        if unlock is not None:
            if unlock in recovery_groups:
                problems.append(f"{where}: Recovery codes must only be supplied on demand in the speaker window")
            if unlock not in group_ids:
                problems.append(f"{where}: data-unlock {unlock!r} is not a known group")
            else:
                unlocks[unlock] = unlocks.get(unlock, 0) + 1
                if "data-minute" in a and (not a["data-minute"].isdigit()
                                           or int(a["data-minute"]) != int(group_ids[unlock]["minute"])):
                    problems.append(f"{where}: unlock slide data-minute does not match group minute")
                if effective in plan_start and int(group_ids[unlock]["minute"]) != plan_start[effective]:
                    problems.append(f"{where}: unlock minute {group_ids[unlock]['minute']} != segment "
                                    f"{effective} start {plan_start[effective]}")
    for g in groups:
        if g["id"] in recovery_groups:
            continue  # Only the speaker window supplies these codes on demand.
        if unlocks.get(g["id"], 0) < 1:
            problems.append(f"group {g['id']!r} has no data-unlock slide")
    used = {s["attrs"].get("data-seg") for s in slides}
    for seg, *_rest in plan:
        if seg not in used:
            problems.append(f"plan segment {seg} has no slide")
    if problems:
        raise BuildError("Deck validation failed", problems)
    return slides


def deck_sources(materials: Path) -> dict:
    src = materials / "facilitator-deck" / "src"
    slide_files = sorted(p for p in (src / "slides").glob("*.html") if not p.name.startswith("00-engine-demo"))
    script_files = sorted((src / "js").glob("*.js"))
    return {"template": src / "deck.template.html", "style": src / "deck.css", "scripts": script_files,
            "slides": slide_files, "codes": materials / "unlock-codes.json"}


JS_PLAN_ROW = re.compile(r'\{\s*seg:\s*"([^"]+)",\s*label:\s*"([^"]*)",\s*start:\s*(\d+),\s*end:\s*(\d+)\s*\}')


def js_plan_problems(script: str, plan) -> list[str]:
    """The deck runtime keeps its own JS PLAN (per-edition js/ directory); it must equal the edition plan."""
    rows = tuple((seg, int(a), int(b), label) for seg, label, a, b in JS_PLAN_ROW.findall(script))
    if rows and rows != tuple(tuple(p) for p in plan):
        return [f"deck js PLAN {rows} differs from edition plan {tuple(plan)}"]
    return []


def build_deck(materials: Path | None = None, edition: Edition = MAIN) -> tuple[bytes, dict]:
    materials = edition.materials if materials is None else materials
    paths = deck_sources(materials)
    missing = [str(p) for k, p in paths.items() if k not in ("slides", "scripts") and not Path(p).exists()]
    if not paths["scripts"]:
        missing.append(str(materials / "facilitator-deck/src/js/*.js"))
    if not paths["slides"]:
        missing.append(str(materials / "facilitator-deck/src/slides/*.html"))
    if missing:
        raise BuildError("Deck sources missing", missing)
    groups = load_codes(materials, edition.recovery_groups)
    template, style = read_text(paths["template"]), read_text(paths["style"])
    script = "\n;\n".join(read_text(p) for p in paths["scripts"])
    parts, slides = [], []
    for path in paths["slides"]:
        text = read_text(path)
        parser = _SlideParser()
        parser.feed(text)
        parser.close()
        for s in parser.slides:
            s["file"] = path.name
        slides.extend(parser.slides)
        parts.append(text.rstrip("\n"))
    slides_html = "\n".join(parts) + "\n"
    validate_slides(slides, groups, edition=edition)
    if js_plan_problems(script, edition.plan):
        raise BuildError("Deck validation failed", js_plan_problems(script, edition.plan))
    if re.search(r"</script", script, re.I):
        raise BuildError("deck scripts must not contain a literal </script")
    inputs = [("template", template.encode()), ("style", style.encode()),
              ("codes", read_bytes(paths["codes"])), ("builder", read_bytes(Path(__file__)))]
    inputs += [("js/" + p.name, read_bytes(p)) for p in paths["scripts"]]
    inputs += [("slides/" + p.name, read_bytes(p)) for p in paths["slides"]]
    digest = inputs_digest(inputs)
    info = f"build {digest[:16]} inputs-sha256 {digest}"
    out = fill_template(template, {"STYLE": style, "SCRIPT": script, "SLIDES": slides_html,
                                   "CODES_JSON": script_safe_json(groups), "BUILD_INFO": info})
    data = out.encode("utf-8")
    summary = {"slides": len(slides), "files": [p.name for p in paths["slides"]], "bytes": len(data),
               "scripts": [p.name for p in paths["scripts"]],
               "unlock_slides": sum(1 for s in slides if "data-unlock" in s["attrs"]),
               "reveal_slides": sum(1 for s in slides if s["attrs"].get("data-seg") == "reveal"),
               "inputs_sha256": digest}
    return data, summary


# ---------------------------------------------------------------- runbook (A)

def md_module():
    """Import the concurrently maintained Markdown module lazily (tests may inject a stub)."""
    import materials_md  # noqa: WPS433
    return materials_md


class Candidate:
    """Read-only access to hash-verified participant ZIPs of the controlled candidate."""

    def __init__(self, directory: Path = CANDIDATE, recovery_downloads: dict = RECOVERY_DOWNLOADS):
        self.directory = Path(directory)
        self.recovery_downloads = recovery_downloads
        evidence_path = self.directory / "build-evidence.json"
        if not Path(long_path(evidence_path)).exists():
            raise BuildError("Candidate evidence missing", [str(evidence_path)])
        self.evidence_bytes = read_bytes(evidence_path)
        evidence = json.loads(self.evidence_bytes.decode("utf-8"))
        self.packages = {p["id"]: p for p in evidence.get("packages", [])}
        self._zips: dict[str, bytes] = {}
        self._members: dict[str, dict[str, bytes]] = {}

    def zip_bytes(self, name: str) -> bytes:
        if name in self._zips:
            return self._zips[name]
        if name not in self.recovery_downloads and not re.fullmatch(r"participant-[a-z0-9-]+\.zip", name or ""):
            raise BuildError("Only participant-*.zip packages may be used", [repr(name)])
        package_id = name[:-4]
        package = self.packages.get(package_id)
        if package is None:
            raise BuildError("Package not listed in build-evidence.json", [name])
        if package.get("role") != "participant":
            raise BuildError("Package is not a participant package", [name])
        if name in self.recovery_downloads:
            expected_minute = self.recovery_downloads[name][1]
            # B1/B2 source versions exist only in the main course; other editions check the minute alone.
            expected_version = {"recovery-52-b1.zip": "B1", "recovery-63-b2.zip": "B2"}.get(name)
            if package.get("release_minute") != expected_minute or (
                    expected_version and package.get("source_version") != expected_version):
                raise BuildError("Recovery package release minute or source version mismatch", [name])
        data = read_bytes(self.directory / name)
        actual = sha256_hex(data)
        if actual != package.get("zip_sha256"):
            raise BuildError("ZIP SHA256 mismatch against build-evidence.json",
                             [f"{name}: expected {package.get('zip_sha256')} actual {actual}"])
        self._zips[name] = data
        return data

    def members(self, name: str) -> dict[str, bytes]:
        if name not in self._members:
            data = self.zip_bytes(name)
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                names = archive.namelist()
                if len(names) != len(set(names)):
                    raise BuildError("Duplicate ZIP member", [name])
                self._members[name] = {build_delivery.safe_path(n).as_posix(): archive.read(n) for n in names}
        return self._members[name]

    def read_member(self, name: str, path: str) -> bytes:
        if name in self.recovery_downloads:
            raise BuildError("Recovery packages are download-only", [name])
        members = self.members(name)
        if path not in members:
            raise BuildError("Included path not in ZIP", [f"{name}:{path}"])
        return members[path]


FENCE_ARGS = re.compile(r"(\w+)=(\S+)")


def scan_fence_args(body: str, kind: str) -> list[dict]:
    """Find ```<kind> fences and parse their key=value first line (used for pre-scan only)."""
    found = []
    for m in re.finditer(r"^```" + kind + r"[ \t]*\r?\n(.*?)\r?\n", body, re.M):
        found.append(dict(FENCE_ARGS.findall(m.group(1))))
    return found


REQUIRED_FM = ("id", "title", "minute", "group", "section")


def load_chapters(content_dir: Path, group_ids: set[str]) -> list[dict]:
    md = md_module()
    files = sorted(Path(content_dir).glob("*.md"))
    if not files:
        raise BuildError("No runbook chapters found", [str(content_dir)])
    problems, chapters, seen = [], [], {}
    for path in files:
        text = read_text(path)
        try:
            meta, body = md.parse_front_matter(text)
        except Exception as exc:  # MarkdownError or malformed front matter
            problems.append(f"{path.name}: front matter error: {exc}")
            continue
        meta = {k: ("" if v is None else str(v)).strip() for k, v in (meta or {}).items()}
        for key in REQUIRED_FM:
            if not meta.get(key):
                problems.append(f"{path.name}: front matter lacks {key}")
        pid, group = meta.get("id", ""), meta.get("group", "")
        if pid and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", pid):
            problems.append(f"{path.name}: id {pid!r} must match [a-z0-9-]")
        if pid in seen:
            problems.append(f"{path.name}: duplicate id {pid!r} (also {seen[pid]})")
        seen[pid] = path.name
        if group and group != "open" and group not in group_ids:
            problems.append(f"{path.name}: group {group!r} not in open + unlock groups")
        chapters.append({"file": path.name, "path": path, "text": text, "body": body,
                         **{k: meta.get(k, "") for k in REQUIRED_FM}})
    if problems:
        raise BuildError("Invalid runbook chapters", problems)
    return chapters


def nav_order(chapters: list[dict]) -> list[dict]:
    sections: dict[str, list[dict]] = {}
    for ch in chapters:
        sections.setdefault(ch["section"], []).append(ch)
    return [ch for items in sections.values() for ch in items]


class LinkResolver:
    """Resolve page links: '#id' -> '#p-id'; '<...>/name.md' -> page including that basename."""

    def __init__(self, page_ids: list[str], includes_by_page: dict[str, list[str]]):
        self.page_ids = list(page_ids)
        self.known = set(page_ids)
        self.by_basename: dict[str, list[str]] = {}
        self.include_sources: set[str] = set()
        for pid in self.page_ids:
            for src in includes_by_page.get(pid, []):
                zip_name, _, path = src.partition(":")
                self.include_sources.update({src, path})
                base = path.rsplit("/", 1)[-1]
                if pid not in self.by_basename.setdefault(base, []):
                    self.by_basename[base].append(pid)
        self.unresolved: list[str] = []

    def is_include(self, source) -> bool:
        return source is not None and (str(source) in self.include_sources or ":" in str(source))

    def resolve(self, page_id: str, href: str, source=None):
        href = (href or "").strip().strip("<>")
        if not href:
            return None
        if re.match(r"https?://", href, re.I):
            if LOCAL_URL_RE.match(href):
                return None
            raise BuildError("External link not allowed", [f"[{page_id}] {href}"])
        if re.match(r"[a-z][a-z0-9+.-]*:", href, re.I):
            return None
        if href.startswith("#"):
            target = href[1:]
            if target.startswith("p-") and target[2:] in self.known:
                return href
            if target in self.known:
                return "#p-" + target
            if self.is_include(source):
                self.unresolved.append(f"[{page_id}] in-document anchor {href} from {source} (rendered as text)")
                return None
            raise BuildError("Unknown page link", [f"[{page_id}] {href}"])
        path = unquote(href.split("#", 1)[0].split("?", 1)[0])
        if path.lower().endswith(".md"):
            base = path.replace("\\", "/").rsplit("/", 1)[-1]
            pages = self.by_basename.get(base, [])
            if not pages:
                self.unresolved.append(f"[{page_id}] {href} (no page includes {base})")
                return None
            return "#p-" + (page_id if page_id in pages else pages[0])
        return None


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def render_nav(ordered: list[dict]) -> str:
    sections: dict[str, list[dict]] = {}
    for ch in ordered:
        sections.setdefault(ch["section"], []).append(ch)
    out = ['<nav class="rb-nav">']
    for title, items in sections.items():
        out.append('  <div class="rb-nav-section">')
        out.append(f'    <div class="rb-nav-section-title">{esc(title)}</div>')
        out.append('    <ul class="rb-nav-list">')
        for ch in items:
            out.append(f'      <li><a class="rb-nav-link" href="#p-{esc(ch["id"])}" data-page="{esc(ch["id"])}" '
                       f'data-group="{esc(ch["group"])}"><span class="rb-nav-title">{esc(ch["title"])}</span>'
                       f'<span class="rb-badge rb-badge-min">{esc(ch["minute"].replace("-", "–"))}</span>'
                       '<span class="rb-nav-state" aria-hidden="true"></span></a></li>')
        out.append('    </ul>')
        out.append('  </div>')
    out.append('</nav>')
    return "\n".join(out)


def render_article(ch: dict, inner: str, locked: bool) -> str:
    body = f'<div class="rb-lock" data-group="{esc(ch["group"])}"></div>' if locked else inner
    return (f'<article class="rb-page" id="p-{esc(ch["id"])}" data-page="{esc(ch["id"])}" '
            f'data-group="{esc(ch["group"])}" data-title="{esc(ch["title"])}" data-minute="{esc(ch["minute"])}" '
            f'data-section="{esc(ch["section"])}" hidden>\n<div class="rb-page-body">{body}</div>\n</article>')


def runbook_sources(materials: Path) -> dict:
    base = materials / "participant-runbook"
    return {"template": base / "template" / "runbook.template.html", "style": base / "template" / "runbook.css",
            "script": base / "template" / "runbook.js", "content": base / "content",
            "codes": materials / "unlock-codes.json"}


def render_pages(ordered: list[dict], candidate: Candidate, group_ids: set[str]):
    """Render every page; returns (inner html by id, downloads by group, used zips, resolver)."""
    md = md_module()
    recovery_downloads = candidate.recovery_downloads
    recovery_groups = {g: m for g, m in recovery_downloads.values()}
    includes_by_page = {ch["id"]: [f"{a.get('zip')}:{a.get('path')}" for a in scan_fence_args(ch["body"], "include")]
                        for ch in ordered}
    resolver = LinkResolver([ch["id"] for ch in ordered], includes_by_page)
    rendered: dict[str, str] = {}
    downloads: dict[str, dict[str, str]] = {}
    download_ids: dict[str, str] = {}
    used_zips: set[str] = set()
    problems: list[str] = []
    for ch in ordered:
        pid, group = ch["id"], ch["group"]
        errors: list[str] = []

        def resolve_link(href, source=None, _pid=pid, _errors=errors):
            try:
                return resolver.resolve(_pid, href, source)
            except BuildError as exc:
                _errors.extend(exc.problems or [str(exc)])
                return None

        def load_include(zip_name, path, _pid=pid, _errors=errors):
            try:
                data = candidate.read_member(zip_name, path)
                used_zips.add(zip_name)
                return data.decode("utf-8")
            except (BuildError, UnicodeDecodeError, ValueError) as exc:
                _errors.append(f"[{_pid}] include {zip_name}:{path}: {exc}")
                raise

        def register_download(download_id, zip_name, label=None, _pid=pid, _group=group, _errors=errors):
            if zip_name in recovery_downloads and _group != recovery_downloads[zip_name][0]:
                raise BuildError("Recovery download requires its independent unlock group", [zip_name, _group])
            if _group in recovery_groups and zip_name not in recovery_downloads:
                raise BuildError("Recovery group may only download its matching recovery package", [zip_name, _group])
            if _group == "open":
                _errors.append(f"[{_pid}] downloads are not allowed on open pages ({download_id})")
                raise BuildError(f"download {download_id} on open page {_pid}")
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(download_id)):
                _errors.append(f"[{_pid}] invalid download id {download_id!r}")
            if download_id in download_ids:
                _errors.append(f"[{_pid}] duplicate download id {download_id!r} (also {download_ids[download_id]})")
            download_ids[download_id] = _pid
            data = candidate.zip_bytes(zip_name)
            used_zips.add(zip_name)
            downloads.setdefault(_group, {})[download_id] = base64.b64encode(data).decode("ascii")
            return {"size_kb": max(1, round(len(data) / 1024)), "sha12": sha256_hex(data)[:12]}

        ctx = md.RenderContext(pid, resolve_link, load_include, register_download)
        try:
            rendered[pid] = md.render_markdown(ch["body"], ctx)
        except Exception as exc:  # MarkdownError, BuildError raised by callbacks, etc.
            if not errors:
                errors.append(f"[{pid}] {ch['file']}: {type(exc).__name__}: {exc}")
        problems.extend(errors)
    if problems:
        raise BuildError("Runbook rendering failed", problems)
    return rendered, downloads, used_zips, resolver


def build_runbook(materials: Path | None = None, candidate_dir: Path | None = None,
                  candidate_id: str | None = None, exemptions=None, edition: Edition = MAIN) -> tuple[bytes, dict]:
    materials = edition.materials if materials is None else materials
    candidate_dir = edition.candidate_dir if candidate_dir is None else candidate_dir
    candidate_id = edition.candidate_id if candidate_id is None else candidate_id
    exemptions = edition.marker_exemptions if exemptions is None else exemptions
    paths = runbook_sources(materials)
    missing = [str(p) for p in paths.values() if not Path(p).exists()]
    if missing:
        raise BuildError("Runbook sources missing", missing)
    groups = load_codes(materials, edition.recovery_groups)
    group_by_id = {g["id"]: g for g in groups}
    chapters = load_chapters(paths["content"], set(group_by_id))
    ordered = nav_order(chapters)
    candidate = Candidate(candidate_dir, edition.recovery_downloads)
    rendered, downloads, used_zips, resolver = render_pages(ordered, candidate, set(group_by_id))
    template, style, script = (read_text(paths[k]) for k in ("template", "style", "script"))
    if re.search(r"</script", script, re.I):
        raise BuildError("runbook.js must not contain a literal </script")
    # Template and runbook.js spell localStorage keys as '{{STORAGE_PREFIX}}theme' etc.; substituted here so
    # each edition keeps its own keys (main stays 'stw:' for existing participant data).
    template_out = template.replace(STORAGE_PREFIX_TOKEN, edition.storage_prefix)
    script_out = script.replace(STORAGE_PREFIX_TOKEN, edition.storage_prefix)
    if edition.storage_prefix != "stw:" and re.search(r"['\"`]stw:", template_out + script_out):
        raise BuildError("Hard-coded 'stw:' storage key; use " + STORAGE_PREFIX_TOKEN, [edition.name])

    articles, group_pages = [], {}
    for ch in ordered:
        locked = ch["group"] != "open"
        if locked:
            group_pages.setdefault(ch["group"], []).append(ch["id"])
        articles.append(render_article(ch, rendered[ch["id"]], locked))
    data_groups, payload_sizes = [], {}
    for g in groups:
        ids = group_pages.get(g["id"], [])
        if not ids:
            continue
        obj = {"pages": {pid: rendered[pid] for pid in ids}, "downloads": downloads.get(g["id"], {})}
        payload = encode_payload(g["id"], g["code"], obj)
        ver = verifier(g["id"], g["code"])
        if decode_payload(g["id"], g["code"], payload, ver) != json.loads(json.dumps(obj, sort_keys=True)):
            raise BuildError("Scheme B round trip failed", [g["id"]])
        payload_sizes[g["id"]] = len(payload)
        data_groups.append({"id": g["id"], "label": g["label"], "minute": g["minute"], "verifier": ver,
                            "payload": payload, "pages": ids})
    stray = sorted(set(downloads) - set(group_pages))
    if stray:
        raise BuildError("Downloads registered for groups without pages", stray)

    inputs = [("template", template.encode()), ("style", style.encode()), ("script", script.encode()),
              ("codes", read_bytes(paths["codes"])), ("builder", read_bytes(Path(__file__))),
              ("candidate/build-evidence.json", candidate.evidence_bytes)]
    md_file = getattr(md_module(), "__file__", None)
    if md_file and Path(md_file).exists():
        inputs.append(("materials_md", read_bytes(Path(md_file))))
    inputs += [("content/" + ch["file"], ch["text"].encode("utf-8")) for ch in chapters]
    inputs += [("zip/" + name, candidate.zip_bytes(name)) for name in sorted(used_zips)]
    digest = inputs_digest(inputs)
    data = {"pages": [{"id": ch["id"], "title": ch["title"], "section": ch["section"], "minute": ch["minute"],
                       "group": ch["group"]} for ch in ordered],
            "groups": data_groups,
            "build": {"source_candidate": candidate_id, "inputs_sha256": digest}}
    nav = render_nav(ordered)
    data_html = '<script id="rb-data" type="application/json">' + script_safe_json(data) + "</script>"
    info = f"候選包 {esc(candidate_id)} · build {digest[:12]}"
    document = fill_template(template_out, {"STYLE": style, "SCRIPT": script_out, "NAV": nav,
                                        "PAGES": "\n".join(articles), "DATA": data_html, "BUILD_INFO": info})

    # ---- safety (4a-4d)
    problems: list[str] = []
    problems += check_codes(document, groups)
    open_texts = [visible_text(rendered[ch["id"]]) for ch in ordered if ch["group"] == "open"]
    open_corpus = " \n ".join(open_texts + [visible_text(nav), " ".join(ch["title"] for ch in ordered)])
    locked_html = {ch["id"]: rendered[ch["id"]] for ch in ordered if ch["group"] != "open"}
    problems += check_plaintext_windows(document, locked_html, open_corpus,
                                        strip=tuple(g["payload"] for g in data_groups))
    texts = {ch["id"]: ch["title"] + "\n" + rendered[ch["id"]] for ch in ordered}
    chrome = {"template": template_out, "runbook.css": style, "runbook.js": script_out, "nav": nav, "build-info": info}
    exempted: list[str] = []
    forbidden = scan_forbidden({**texts, **chrome}, edition.forbidden_markers, exemptions=exemptions, exempted=exempted)
    urls = scan_urls(texts) + scan_urls(chrome, allow_namespaces=True)
    b0_hits = scan_b0_policy(ordered, rendered, {g["id"]: int(g["minute"]) for g in groups}) if edition.b0_guard else []
    b0_zip = "participant-29-b0.zip"
    if edition.b0_guard and b0_zip in used_zips:
        members = dict(candidate.members(b0_zip))
        members.pop("PACKAGE-MANIFEST.json", None)
        try:
            build_delivery.content_policy({"id": "participant-29-b0", "role": "participant"}, members)
        except ValueError as exc:
            b0_hits.append(f"[{b0_zip}] build_delivery.content_policy: {exc}")
    problems += forbidden + urls + b0_hits
    if problems:
        raise BuildError("Runbook safety checks failed", problems)

    out = document.encode("utf-8")
    summary = {"pages": len(ordered),
               "pages_per_group": {gid: len([c for c in ordered if c["group"] == gid])
                                   for gid in ["open"] + [g["id"] for g in groups]},
               "payload_chars": payload_sizes, "downloads": {g: sorted(d) for g, d in downloads.items()},
               "used_zips": sorted(used_zips), "bytes": len(out), "inputs_sha256": digest,
               "notes": list(resolver.unresolved), "exempted_markers": exempted,
               "safety": {"codes": "clean", "plaintext_windows": "clean", "forbidden_hits": 0,
                          "external_urls": 0, "b0_policy": "clean" if edition.b0_guard and b0_zip in used_zips else "not applicable"}}
    return out, summary


# ---------------------------------------------------------------- CLI

def outputs(materials: Path = MATERIALS) -> dict[str, Path]:  # same file names in every edition's materials dir
    return {"deck": materials / "facilitator-deck" / "facilitator-deck.html",
            "runbook": materials / "participant-runbook" / "runbook.html"}


def run(check: bool = False, only: str | None = None, materials: Path | None = None,
        candidate_dir: Path | None = None, out_paths: dict[str, Path] | None = None, edition: Edition = MAIN) -> int:
    materials = edition.materials if materials is None else materials
    out_paths = out_paths or outputs(materials)
    targets = [only] if only else ["deck", "runbook"]
    status = 0
    for target in targets:
        if target == "deck":
            data, summary = build_deck(materials, edition)
        else:
            data, summary = build_runbook(materials, candidate_dir, edition=edition)
        path = out_paths[target]
        rel = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        if check:
            current = read_bytes(path) if path.exists() else None
            same = current == data
            print(f"[{target}] {'UP-TO-DATE' if same else 'DIFFERS'} {rel} ({len(data):,} bytes built"
                  f"{'' if current is None else f', {len(current):,} on disk'})")
            if not same:
                status = 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(long_path(path), "wb") as handle:
                handle.write(data)
            print(f"[{target}] wrote {rel} ({len(data):,} bytes, {len(data) / 1024:.1f} KB)")
        print_summary(target, summary)
    return status


def print_summary(target: str, summary: dict) -> None:
    if target == "deck":
        print(f"  slides={summary['slides']} unlock={summary['unlock_slides']} reveal={summary['reveal_slides']}"
              f" files={len(summary['files'])} inputs={summary['inputs_sha256'][:16]}")
        return
    per_group = ", ".join(f"{g}={n}" for g, n in summary["pages_per_group"].items())
    payloads = ", ".join(f"{g}={n:,}" for g, n in summary["payload_chars"].items())
    dls = ", ".join(g + ":" + "/".join(ids) for g, ids in summary["downloads"].items())
    zips = summary["used_zips"]
    print("  pages per group: " + per_group)
    print("  payload chars:   " + payloads)
    print("  downloads:       " + dls)
    print(f"  zips used:       {len(zips)} (" + ", ".join(zips) + ")")
    print("  safety:          " + json.dumps(summary["safety"], ensure_ascii=False))
    for item in summary["exempted_markers"]:
        print("  EXEMPTED: " + item)
    for note in summary["notes"]:
        print("  note: " + note)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build facilitator deck and participant runbook HTML.")
    parser.add_argument("--check", action="store_true", help="rebuild in memory and compare with disk")
    parser.add_argument("--only", choices=("deck", "runbook"))
    parser.add_argument("--edition", choices=("main", "dlc"), default="main",
                        help="main = 90-min course (materials/); dlc = DDD DLC (materials-dlc/)")
    args = parser.parse_args(argv)
    try:
        return run(check=args.check, only=args.only, edition=load_edition(args.edition))
    except BuildError as exc:
        print("BUILD FAILED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
