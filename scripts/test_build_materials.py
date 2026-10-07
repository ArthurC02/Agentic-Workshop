"""Tests for build_materials.py (stdlib unittest). Run:
    python -X utf8 -m unittest scripts/test_build_materials.py -v
"""
from __future__ import annotations

import base64
import dataclasses
import hashlib
import html as html_mod
import io
import json
import re
import shutil
import sys
import tempfile
import types
import unittest
import zipfile
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import build_materials as bm  # noqa: E402

try:
    import materials_md as REAL_MD  # noqa: E402
except Exception:  # module missing or still being written
    REAL_MD = None


# ---------------------------------------------------------------- minimal Markdown stub (tests only)

def _stub_module():
    mod = types.ModuleType("materials_md_stub")

    class MarkdownError(ValueError):
        pass

    @dataclasses.dataclass
    class RenderContext:
        page_id: str
        resolve_link: object
        load_include: object
        register_download: object
        task_counter: int = 0

    def parse_front_matter(text):
        lines = text.replace("\r\n", "\n").split("\n")
        if not lines or lines[0].strip() != "---":
            return {}, text
        meta = {}
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return meta, "\n".join(lines[i + 1:])
            key, _, value = lines[i].partition(":")
            meta[key.strip()] = value.strip()
        raise MarkdownError("unterminated front matter")

    def inline(text, ctx, source):
        out, pos = [], 0
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
            out.append(html_mod.escape(text[pos:m.start()]))
            target = ctx.resolve_link(m.group(2), source)
            label = html_mod.escape(m.group(1))
            out.append(f'<a class="rb-xref" href="{target}">{label}</a>' if target else label)
            pos = m.end()
        out.append(html_mod.escape(text[pos:]))
        return "".join(out)

    def render_markdown(md, ctx, heading_shift=1, source=None):
        out, lines, i = [], md.replace("\r\n", "\n").split("\n"), 0
        while i < len(lines):
            line = lines[i]
            fence = re.match(r"^```(\w+)", line)
            if fence:
                j = i + 1
                while j < len(lines) and not lines[j].startswith("```"):
                    j += 1
                block = lines[i + 1:j]
                args = dict(re.findall(r"(\w+)=(\S+)", block[0] if block else ""))
                if fence.group(1) == "include":
                    text = ctx.load_include(args["zip"], args["path"])
                    inner = render_markdown(text, ctx, heading_shift + 1, args["zip"] + ":" + args["path"])
                    out.append(f'<section class="rb-include">{inner}</section>')
                elif fence.group(1) == "download":
                    label = block[0].split("label=", 1)[-1]
                    info = ctx.register_download(args["id"], args["zip"], label)
                    out.append(f'<div class="rb-download-card"><button data-download="{args["id"]}">'
                               f'{html_mod.escape(label)}</button><span>ZIP · {info["size_kb"]} KB · '
                               f'SHA256 {info["sha12"]}</span></div>')
                else:
                    out.append("<pre><code>" + html_mod.escape("\n".join(block)) + "</code></pre>")
                i = j + 1
                continue
            heading = re.match(r"^(#+)\s+(.*)", line)
            if heading:
                level = min(6, len(heading.group(1)) + heading_shift)
                out.append(f"<h{level}>{inline(heading.group(2), ctx, source)}</h{level}>")
            elif line.strip():
                out.append(f"<p>{inline(line, ctx, source)}</p>")
            i += 1
        return "\n".join(out)

    mod.MarkdownError = MarkdownError
    mod.RenderContext = RenderContext
    mod.parse_front_matter = parse_front_matter
    mod.render_markdown = render_markdown
    return mod


STUB = _stub_module()


def use_stub():
    return mock.patch.object(bm, "md_module", lambda: STUB)


# ---------------------------------------------------------------- fixtures

GROUPS = [{"id": "greenfield", "minute": 7, "code": "GF-ALPHA-07", "label": "Greenfield"},
          {"id": "b1", "minute": 44, "code": "B1-BRAVO-44", "label": "B1"}]
SEG_TITLES = [(seg, start) for seg, start, _end, _label in bm.PLAN]


def slide(seg, title, extra="", notes=True):
    aside = '<aside class="notes"><p>cue</p></aside>' if notes else ""
    return f'<section class="slide" data-seg="{seg}" data-title="{title}"{extra}><h2>{title}</h2>{aside}</section>\n'


def good_slides():
    out = []
    for seg, start in SEG_TITLES:
        extra = f' data-minute="{start:02d}"'
        if seg == "greenfield":
            out.append(slide(seg, "Unlock GF", extra + ' data-unlock="greenfield"'))
        if seg == "b1":
            out.append(slide(seg, "Unlock B1", extra + ' data-unlock="b1"'))
        out.append(slide(seg, f"Seg {seg}", extra + (' data-timer="22:00"' if seg == "greenfield" else "")))
        if seg == "greenfield":
            out.append(slide("reveal", "Reveal GF", ' data-reveal-of="greenfield"'))
    return "".join(out)


OPEN_TEXT = "Welcome to the workshop. Read the [environment](#env) page before the first unlock happens today."
LOCKED_TEXT = "This greenfield mission text is secret until the facilitating host announces the unlock moment."


def chapter(pid, title, group, section, body, minute="00-07"):
    return f"---\nid: {pid}\ntitle: {title}\nminute: {minute}\ngroup: {group}\nsection: {section}\n---\n{body}\n"


def make_zip(members: dict[str, str]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, text in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            archive.writestr(info, text.encode("utf-8"))
    return buf.getvalue()


class Fixture:
    """A self-contained materials tree + candidate directory in a temp folder."""

    def __init__(self, root: Path):
        self.root = root
        self.materials = root / "materials"
        self.candidate = root / "candidate"
        deck = self.materials / "facilitator-deck" / "src"
        (deck / "slides").mkdir(parents=True)
        (deck / "deck.template.html").write_text(
            "<html><!-- {{BUILD_INFO}} --><style>{{STYLE}}</style><div id=\"dk-stage\">{{SLIDES}}</div>"
            "<script>window.DECK_CODES = {{CODES_JSON}};</script><script>{{SCRIPT}}</script></html>\n",
            encoding="utf-8")
        (deck / "deck.css").write_text(".slide{display:block}\n", encoding="utf-8")
        (deck / "js").mkdir()
        (deck / "js" / "20-features.js").write_text("var feature = 2;\n", encoding="utf-8")
        (deck / "js" / "10-core.js").write_text("console.log('deck {{STYLE}} literal stays');\n", encoding="utf-8")
        (deck / "js" / "notes.txt").write_text("ignored", encoding="utf-8")
        (deck / "slides" / "10-all.html").write_text(good_slides(), encoding="utf-8")
        (deck / "slides" / "00-engine-demo.html").write_text('<section class="slide" data-seg="bogus"></section>',
                                                             encoding="utf-8")
        rb = self.materials / "participant-runbook"
        (rb / "template").mkdir(parents=True)
        (rb / "content").mkdir(parents=True)
        (rb / "template" / "runbook.template.html").write_text(
            "<html><style>{{STYLE}}</style><aside>{{NAV}}<div>{{BUILD_INFO}}</div></aside>"
            "<main>{{PAGES}}</main>{{DATA}}<script>{{SCRIPT}}</script></html>\n", encoding="utf-8")
        (rb / "template" / "runbook.css").write_text(".rb-page{color:#123}\n", encoding="utf-8")
        (rb / "template" / "runbook.js").write_text(
            "var ns='http://www.w3.org/2000/svg'; window.RB={version:1};\n", encoding="utf-8")
        self.content = rb / "content"
        self.write_chapter("00-welcome.md", chapter("welcome", "Welcome", "open", "Start", OPEN_TEXT))
        self.write_chapter("01-env.md", chapter("env", "Environment", "open", "Start",
                                                "Run the API at http://127.0.0.1:8000/docs locally."))
        self.write_chapter("10-gf.md", chapter(
            "gf", "Greenfield", "greenfield", "Greenfield", LOCKED_TEXT + "\n\nSee [mission](#gf-mission).\n\n"
            "```download\nid=g0 zip=participant-07-demo.zip label=Download G0\n```", minute="07-29"))
        self.write_chapter("11-gf-mission.md", chapter(
            "gf-mission", "Mission", "greenfield", "Greenfield",
            "```include\nzip=participant-07-demo.zip path=demo/participant/01-mission.md\n```", minute="07-29"))
        self.write_chapter("44-b1.md", chapter(
            "b1", "B1 task", "b1", "Brownfield", "B1 body text is only for the forty-four minute reveal point.",
            minute="44-52"))
        self.write_codes(GROUPS)
        self.candidate.mkdir()
        self.zips = {}
        self.add_zip("participant-07-demo", {
            "demo/participant/01-mission.md": "# Mission\n\nBuild the MVP. Back to [the task](../../x/02-task.md#top).\n"
                                              "Jump to [escalation](#escalation).\n",
            "demo/participant/src/app.py": "print('hi')\n"})
        self.add_zip("evaluation-private", {"x.md": "secret"}, role="evaluation")
        self.write_evidence()

    def write_chapter(self, name, text):
        (self.content / name).write_text(text, encoding="utf-8")

    def write_codes(self, groups):
        (self.materials / "unlock-codes.json").write_text(json.dumps({"groups": groups}), encoding="utf-8")

    def add_zip(self, package_id, members, role="participant"):
        data = make_zip(members)
        (self.candidate / (package_id + ".zip")).write_bytes(data)
        self.zips[package_id] = (role, data)

    def write_evidence(self, override=None):
        packages = [{"id": pid, "role": role, "zip": pid + ".zip",
                     "zip_sha256": (override or {}).get(pid, hashlib.sha256(data).hexdigest()),
                     "zip_bytes": len(data)} for pid, (role, data) in self.zips.items()]
        (self.candidate / "build-evidence.json").write_text(json.dumps({"packages": packages}), encoding="utf-8")

    def outputs(self):
        return {"deck": self.root / "out" / "deck.html", "runbook": self.root / "out" / "runbook.html"}


class FixtureCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.fx = Fixture(Path(self._tmp.name))
        self._stub = use_stub()
        self._stub.start()

    def tearDown(self):
        self._stub.stop()
        self._tmp.cleanup()

    def build_runbook(self):
        return bm.build_runbook(self.fx.materials, self.fx.candidate, "testcand")


# ---------------------------------------------------------------- scheme B

class RecoveryTests(FixtureCase):
    def setUp(self):
        super().setUp()
        self.groups = GROUPS + [{"id": "recovery-b1", "minute": 52, "code": "REC-ONE-52", "label": "Recovery B1"},
                                {"id": "recovery-b2", "minute": 63, "code": "REC-TWO-63", "label": "Recovery B2"}]
        self.fx.write_codes(self.groups)
        for name, (group, minute) in bm.RECOVERY_DOWNLOADS.items():
            self.fx.add_zip(name[:-4], {"context.md": "Recovery-only isolated content"})
        self.fx.write_evidence()
        evidence = json.loads((self.fx.candidate / "build-evidence.json").read_text())
        for p in evidence["packages"]:
            if p["id"] + ".zip" in bm.RECOVERY_DOWNLOADS:
                p.update(release_minute=bm.RECOVERY_DOWNLOADS[p["id"] + ".zip"][1],
                         source_version="B1" if p["id"] == "recovery-52-b1" else "B2")
        self.evidence = evidence
        self.save_evidence()

    def save_evidence(self):
        (self.fx.candidate / "build-evidence.json").write_text(json.dumps(self.evidence), encoding="utf-8")

    def recovery_page(self, group, name, kind="download"):
        args = f"id=resume zip={name} label=Resume" if kind == "download" else f"zip={name} path=context.md"
        return {"id": "resume", "group": group, "body": f"```{kind}\n{args}\n```", "file": "resume.md"}

    def test_exact_names_roles_hash_and_stage(self):
        c = bm.Candidate(self.fx.candidate)
        for name in bm.RECOVERY_DOWNLOADS:
            self.assertEqual(c.zip_bytes(name), (self.fx.candidate / name).read_bytes())
        for name in ("recovery-63-b3.zip", "evaluation-private.zip", "facilitator-private.zip"):
            with self.assertRaises(bm.BuildError):
                c.zip_bytes(name)
        p = next(p for p in self.evidence["packages"] if p["id"] == "recovery-52-b1")
        for key, value in (("role", "evaluation"), ("source_version", "B2"), ("release_minute", 44), ("zip_sha256", "bad")):
            old = p[key]
            p[key] = value
            self.save_evidence()
            with self.assertRaises(bm.BuildError):
                bm.Candidate(self.fx.candidate).zip_bytes("recovery-52-b1.zip")
            p[key] = old

    def test_recovery_download_only_matching_independent_group(self):
        c = bm.Candidate(self.fx.candidate)
        for name, (group, minute) in bm.RECOVERY_DOWNLOADS.items():
            _html, downloads, _zips, _resolver = bm.render_pages([self.recovery_page(group, name)], c, set())
            self.assertEqual(base64.b64decode(downloads[group]["resume"]), c.zip_bytes(name))
            for wrong in ("open", "b1", "b2", "b3", "recovery-b1" if group == "recovery-b2" else "recovery-b2"):
                with self.assertRaises(bm.BuildError):
                    bm.render_pages([self.recovery_page(wrong, name)], c, set())
            with self.assertRaises(bm.BuildError):
                bm.render_pages([self.recovery_page(group, name, "include")], c, set())
            with self.assertRaises(bm.BuildError):
                c.read_member(name, "context.md")

    def test_normal_unlock_code_cannot_open_recovery(self):
        for g in self.groups[-2:]:
            payload = bm.encode_payload(g["id"], g["code"], {"downloads": {"resume": "secret"}})
            for normal in GROUPS:
                with self.assertRaises(ValueError):
                    bm.decode_payload(g["id"], normal["code"], payload, bm.verifier(g["id"], g["code"]))
        self.groups[-1]["code"] = GROUPS[0]["code"]
        self.fx.write_codes(self.groups)
        with self.assertRaises(bm.BuildError):
            bm.load_codes(self.fx.materials)


class SchemeBTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(bm.normalize_code(" g0-start 07 "), "G0START07")
        self.assertEqual(bm.normalize_code("b3_group–63!"), "B3GROUP63")
        self.assertEqual(bm.normalize_code("RETRO-80"), bm.normalize_code("retro80"))

    def test_verifier_matches_spec(self):
        expected = hashlib.sha256("verify:b1:B1FARE44".encode("utf-8")).hexdigest()
        self.assertEqual(bm.verifier("b1", "b1-fare-44"), expected)
        self.assertNotEqual(bm.verifier("b2", "b1-fare-44"), expected)  # salt = group id

    def test_keystream_blocks(self):
        ks = bm.keystream("grp", "ab-1", 70)
        self.assertEqual(len(ks), 70)
        self.assertEqual(ks[:32], hashlib.sha256(b"ks:grp:AB1:0").digest())
        self.assertEqual(ks[32:64], hashlib.sha256(b"ks:grp:AB1:1").digest())
        self.assertEqual(ks[64:70], hashlib.sha256(b"ks:grp:AB1:2").digest()[:6])

    def test_round_trip_and_independent_decode(self):
        obj = {"pages": {"p1": "<p>中文內容 & <b>html</b></p>"}, "downloads": {"z": base64.b64encode(b"\0\1zip").decode()}}
        payload = bm.encode_payload("b2", "B2-best-52", obj)
        self.assertEqual(bm.decode_payload("b2", " b2 best 52 ", payload, bm.verifier("b2", "B2BEST52")), obj)
        # Independent reference decoder written straight from spec A5.
        raw = base64.b64decode(payload)
        key = b"".join(hashlib.sha256(f"ks:b2:B2BEST52:{i}".encode()).digest() for i in range(len(raw) // 32 + 1))
        plain = bytes(a ^ b for a, b in zip(raw, key))
        self.assertEqual(json.loads(plain.decode("utf-8")), obj)
        self.assertNotIn("中文內容", base64.b64decode(payload).decode("utf-8", "replace"))

    def test_wrong_code_rejected(self):
        payload = bm.encode_payload("b1", "RIGHT-1", {"pages": {}, "downloads": {}})
        with self.assertRaises(ValueError):
            bm.decode_payload("b1", "WRONG-1", payload, bm.verifier("b1", "RIGHT-1"))

    def test_empty_xor(self):
        self.assertEqual(bm.xor_bytes(b"", b""), b"")
        self.assertEqual(bm.xor_bytes(b"\x00\x01", b"\xff\xff\xaa"), b"\xff\xfe")


# ---------------------------------------------------------------- links

class LinkResolutionTests(unittest.TestCase):
    def setUp(self):
        includes = {"b3-task-card": ["participant-63-b3-governance.zip:agentic-workshop/03-brownfield/participant/"
                                     "task-cards/03-b3-group-booking.md"],
                    "b3-exception-card": ["participant-63-b3-governance.zip:agentic-workshop/04-digital-worker/"
                                          "participant/06-exception-response-card.md"]}
        self.r = bm.LinkResolver(["welcome", "b3", "b3-task-card", "b3-exception-card"], includes)

    def test_page_anchor(self):
        self.assertEqual(self.r.resolve("welcome", "#b3"), "#p-b3")
        self.assertEqual(self.r.resolve("welcome", "#p-b3"), "#p-b3")

    def test_unknown_page_anchor_is_error(self):
        with self.assertRaises(bm.BuildError):
            self.r.resolve("welcome", "#nope")

    def test_unknown_anchor_inside_include_is_text(self):
        src = "participant-63-b3-governance.zip:agentic-workshop/04-digital-worker/participant/06-exception-response-card.md"
        self.assertIsNone(self.r.resolve("b3-exception-card", "#escalation", src))
        self.assertTrue(self.r.unresolved)

    def test_relative_md_by_basename(self):
        href = "../../03-brownfield/participant/task-cards/03-b3-group-booking.md#scope"
        self.assertEqual(self.r.resolve("b3-exception-card", href, "x.zip:y.md"), "#p-b3-task-card")
        self.assertEqual(self.r.resolve("b3-task-card", "03-b3-group-booking.md"), "#p-b3-task-card")

    def test_unknown_md_and_other_links(self):
        self.assertIsNone(self.r.resolve("b3", "../missing.md"))
        self.assertIsNone(self.r.resolve("b3", "src/app.py"))
        self.assertIsNone(self.r.resolve("b3", "http://127.0.0.1:8000/docs"))
        self.assertIsNone(self.r.resolve("b3", "http://localhost/health"))
        with self.assertRaises(bm.BuildError):
            self.r.resolve("b3", "https://example.com/x")


# ---------------------------------------------------------------- safety scans

class SafetyTests(unittest.TestCase):
    def test_codes_detected_raw_and_normalized(self):
        self.assertTrue(bm.check_codes("<p>code: G0-START-07</p>", [{"id": "g", "code": "G0-START-07"}]))
        self.assertTrue(bm.check_codes("<p>g0start07</p>", [{"id": "g", "code": "G0-START-07"}]))
        self.assertFalse(bm.check_codes("<p>G0 START at 07</p>", [{"id": "g", "code": "G0-START-07"}]))

    def test_plaintext_window_detected(self):
        locked = {"x": "<p>" + LOCKED_TEXT + "</p>"}
        doc = "<main><p>intro</p><p>" + LOCKED_TEXT[20:70] + "</p></main>"
        self.assertTrue(bm.check_plaintext_windows(doc, locked, "open text only"))
        self.assertFalse(bm.check_plaintext_windows("<main>nothing here</main>", locked, ""))
        # Phrasing shared with open pages is legitimate.
        self.assertFalse(bm.check_plaintext_windows(doc, locked, LOCKED_TEXT))

    def test_plaintext_window_across_tags_and_entities(self):
        locked = {"x": "<p>Alpha &amp; beta gamma delta epsilon zeta eta theta</p>"}
        doc = "<p>Alpha &amp; beta <b>gamma delta</b> epsilon zeta eta theta</p>"
        self.assertTrue(bm.check_plaintext_windows(doc, locked, ""))

    def test_forbidden_markers(self):
        hits = bm.scan_forbidden({"p1": "see the Facilitator guide", "p2": "這是標準答案", "p3": "fine",
                                  "p4": "uses student_fare_rate constant"})
        joined = "\n".join(hits)
        self.assertIn("[p1]", joined)
        self.assertIn("[p2]", joined)
        self.assertIn("[p4]", joined)
        self.assertNotIn("[p3]", joined)

    def test_external_urls(self):
        hits = bm.scan_urls({"p": "go https://example.com/a and http://127.0.0.1:8000/docs http://localhost/x"})
        self.assertEqual(len(hits), 1)
        self.assertIn("example.com", hits[0])
        self.assertTrue(bm.scan_urls({"js": "http://www.w3.org/2000/svg"}))
        self.assertFalse(bm.scan_urls({"js": "http://www.w3.org/2000/svg"}, allow_namespaces=True))
        self.assertTrue(bm.scan_urls({"p": "http://localhost.evil.com/"}))

    def test_b0_policy_scan(self):
        pages = [{"id": "early", "group": "timeskip"}, {"id": "late", "group": "b1"}]
        texts = {"early": "<p>學生票 Bug 在這裡</p>", "late": "<p>學生票 Bug 在這裡</p>"}
        hits = bm.scan_b0_policy(pages, texts, {"timeskip": 29, "b1": 44, "b2": 52})
        self.assertEqual(len(hits), 1)
        self.assertIn("[early]", hits[0])


# ---------------------------------------------------------------- deck validation

class DeckValidationTests(unittest.TestCase):
    def assertProblem(self, slides_html, needle, groups=GROUPS):
        with self.assertRaises(bm.BuildError) as cm:
            bm.validate_slides(slides_html, groups)
        self.assertTrue(any(needle in p for p in cm.exception.problems), cm.exception.problems)

    def test_good_slides_pass(self):
        slides = bm.validate_slides(good_slides(), GROUPS)
        self.assertEqual(sum(1 for s in slides if "data-unlock" in s["attrs"]), 2)

    def test_bad_segment(self):
        self.assertProblem(good_slides() + slide("bogus", "Bad"), "data-seg 'bogus'")

    def test_missing_notes(self):
        self.assertProblem(good_slides() + slide("retro", "No notes", notes=False), "missing <aside")

    def test_missing_title(self):
        self.assertProblem(good_slides() + slide("retro", ""), "missing data-title")

    def test_unknown_unlock_group(self):
        self.assertProblem(good_slides() + slide("retro", "X", ' data-unlock="nope"'), "not a known group")

    def test_group_without_unlock_slide(self):
        groups = GROUPS + [{"id": "b2", "minute": 52, "code": "B2-X-52", "label": "B2"}]
        self.assertProblem(good_slides(), "'b2' has no data-unlock slide", groups)

    def test_unlock_minute_mismatch(self):
        groups = [dict(GROUPS[0], minute=8), GROUPS[1]]
        self.assertProblem(good_slides(), "unlock minute 8", groups)

    def test_reveal_requires_reveal_of(self):
        self.assertProblem(good_slides() + slide("reveal", "R"), "lacks data-reveal-of")

    def test_segment_order(self):
        self.assertProblem(good_slides() + slide("opening", "Late opening"), "out of plan order")

    def test_plan_contiguity(self):
        self.assertEqual(bm.plan_problems(), [])
        bad = (("opening", 0, 7, "a"), ("greenfield", 8, 29, "b"), ("retro", 29, 90, "c"))
        self.assertTrue(any("gap/overlap" in p for p in bm.plan_problems(bad)))
        short = (("opening", 0, 7, "a"), ("retro", 7, 80, "c"))
        self.assertTrue(any("90" in p for p in bm.plan_problems(short)))


# ---------------------------------------------------------------- fixture builds

class FixtureBuildTests(FixtureCase):
    def test_deck_build_and_determinism(self):
        first, summary = bm.build_deck(self.fx.materials)
        second, _ = bm.build_deck(self.fx.materials)
        self.assertEqual(first, second)
        text = first.decode("utf-8")
        self.assertNotIn("bogus", text)  # 00-engine-demo* skipped
        self.assertIn("console.log('deck {{STYLE}} literal stays')", text)  # single-pass fill
        self.assertIn('"code":"GF-ALPHA-07"', text)
        self.assertEqual(summary["unlock_slides"], 2)
        # js/*.js concatenated in filename order with "\n;\n"; non-.js files ignored.
        self.assertIn("console.log('deck {{STYLE}} literal stays');\n\n;\nvar feature = 2;",
                      text.replace("\r\n", "\n"))
        self.assertNotIn("ignored", text)
        self.assertEqual(summary["scripts"], ["10-core.js", "20-features.js"])

    def test_deck_requires_js_dir(self):
        shutil.rmtree(self.fx.materials / "facilitator-deck" / "src" / "js")
        with self.assertRaises(bm.BuildError) as cm:
            bm.build_deck(self.fx.materials)
        self.assertIn("src/js/*.js", str(cm.exception).replace("\\", "/"))

    def test_script_safe_json(self):
        text = bm.script_safe_json({"t": "</script><!-- x"})
        self.assertNotIn("<", text)
        self.assertEqual(json.loads(text), {"t": "</script><!-- x"})

    def test_runbook_structure_and_payload(self):
        out, summary = self.build_runbook()
        text = out.decode("utf-8")
        self.assertEqual(out, self.build_runbook()[0])  # deterministic
        self.assertIn('id="p-welcome"', text)
        self.assertIn('<div class="rb-page-body"><div class="rb-lock" data-group="greenfield"></div></div>', text)
        self.assertNotIn("secret until", text)
        self.assertNotIn("Build the MVP", text)
        self.assertIn('href="#p-env"', text)
        data = json.loads(re.search(r'<script id="rb-data" type="application/json">(.*?)</script>', text, re.S)
                          .group(1))
        self.assertEqual([p["id"] for p in data["pages"]], ["welcome", "env", "gf", "gf-mission", "b1"])
        self.assertEqual(data["build"]["source_candidate"], "testcand")
        gf = next(g for g in data["groups"] if g["id"] == "greenfield")
        decoded = bm.decode_payload("greenfield", "gf alpha 07", gf["payload"], gf["verifier"])
        self.assertIn("secret until", decoded["pages"]["gf"])
        self.assertIn('href="#p-gf-mission"', decoded["pages"]["gf"])
        self.assertIn("Build the MVP", decoded["pages"]["gf-mission"])
        self.assertEqual(base64.b64decode(decoded["downloads"]["g0"]), self.fx.zips["participant-07-demo"][1])
        self.assertEqual(summary["pages_per_group"], {"open": 2, "greenfield": 2, "b1": 1})
        self.assertTrue(any("02-task.md" in n for n in summary["notes"]))

    def test_check_mode(self):
        outs = self.fx.outputs()
        self.assertEqual(bm.run(materials=self.fx.materials, candidate_dir=self.fx.candidate, out_paths=outs), 0)
        self.assertEqual(bm.run(check=True, materials=self.fx.materials, candidate_dir=self.fx.candidate,
                                out_paths=outs), 0)
        outs["runbook"].write_bytes(outs["runbook"].read_bytes() + b" ")
        self.assertEqual(bm.run(check=True, only="runbook", materials=self.fx.materials,
                                candidate_dir=self.fx.candidate, out_paths=outs), 1)
        self.assertEqual(bm.run(check=True, only="deck", materials=self.fx.materials,
                                candidate_dir=self.fx.candidate, out_paths=outs), 0)

    def assertBuildFails(self, needle):
        with self.assertRaises(bm.BuildError) as cm:
            self.build_runbook()
        message = str(cm.exception)
        self.assertIn(needle, message)
        return message

    def test_injected_code_fails(self):
        self.fx.write_chapter("02-x.md", chapter("x", "X", "open", "Start", "Psst: gf-alpha-07"))
        self.assertBuildFails("unlock code for group 'greenfield'")

    def test_injected_forbidden_text_fails(self):
        self.fx.write_chapter("02-x.md", chapter("x", "X", "open", "Start", "Ask the Facilitator for the 標準答案."))
        message = self.assertBuildFails("[x] forbidden marker 'facilitator'")
        self.assertIn("標準答案", message)

    def test_locked_page_forbidden_text_fails(self):
        self.fx.write_chapter("45-y.md", chapter("y", "Y", "b1", "Brownfield", "See evaluation notes.", "44-52"))
        self.assertBuildFails("[y] forbidden marker 'evaluation'")

    def test_external_url_fails(self):
        self.fx.write_chapter("02-x.md", chapter("x", "X", "open", "Start", "Visit https://example.com/now"))
        self.assertBuildFails("example.com")

    def test_locked_plaintext_leak_fails(self):
        # Locked text leaking through the shell (here: runbook.js) is caught by the 30-char window check.
        js = self.fx.materials / "participant-runbook" / "template" / "runbook.js"
        js.write_text("var cache = '" + LOCKED_TEXT[10:60] + "';\n", encoding="utf-8")
        self.assertBuildFails("locked page 'gf' plaintext visible")

    def test_download_on_open_page_fails(self):
        self.fx.write_chapter("02-x.md", chapter("x", "X", "open", "Start",
                                                 "```download\nid=dl zip=participant-07-demo.zip label=x\n```"))
        self.assertBuildFails("downloads are not allowed on open pages")

    def test_zip_hash_mismatch_fails(self):
        self.fx.write_evidence({"participant-07-demo": "0" * 64})
        self.assertBuildFails("SHA256 mismatch")

    def test_non_participant_zip_fails(self):
        self.fx.write_chapter("12-z.md", chapter("z", "Z", "greenfield", "Greenfield",
                                                 "```include\nzip=evaluation-private.zip path=x.md\n```", "07-29"))
        self.assertBuildFails("Only participant-*.zip")

    def test_front_matter_validation(self):
        self.fx.write_chapter("02-x.md", chapter("welcome", "Dup", "nogroup", "Start", "x"))
        message = self.assertBuildFails("duplicate id 'welcome'")
        self.assertIn("group 'nogroup'", message)
        self.fx.write_chapter("02-x.md", "---\nid: x\ntitle: T\n---\nbody\n")
        self.assertBuildFails("front matter lacks minute")

    def test_unknown_page_link_fails(self):
        self.fx.write_chapter("02-x.md", chapter("x", "X", "open", "Start", "Go [there](#nowhere)."))
        self.assertBuildFails("#nowhere")

    def test_marker_exemption_is_narrow(self):
        self.fx.write_chapter("02-x.md", chapter("x", "X", "open", "Start", "空白範本不預發標準答案。"))
        _out, summary = bm.build_runbook(self.fx.materials, self.fx.candidate, "testcand",
                                         exemptions=(("x", "不預發標準答案"),))
        self.assertEqual(len(summary["exempted_markers"]), 1)
        # Same phrase on another page, or a second bare occurrence, still fails.
        with self.assertRaises(bm.BuildError):
            bm.build_runbook(self.fx.materials, self.fx.candidate, "testcand", exemptions=(("other", "不預發標準答案"),))
        self.fx.write_chapter("02-x.md", chapter("x", "X", "open", "Start", "不預發標準答案。這是標準答案。"))
        with self.assertRaises(bm.BuildError):
            bm.build_runbook(self.fx.materials, self.fx.candidate, "testcand", exemptions=(("x", "不預發標準答案"),))


# ---------------------------------------------------------------- integration (real sources)

def _real_sources_ready():
    deck = bm.deck_sources(bm.MATERIALS)
    rb = bm.runbook_sources(bm.MATERIALS)
    needed = [deck["template"], deck["style"], rb["template"], rb["style"], rb["script"],
              bm.CANDIDATE / "build-evidence.json"]
    return REAL_MD is not None and bool(deck["scripts"]) and bool(deck["slides"]) and all(p.exists() for p in needed)


@unittest.skipUnless(_real_sources_ready(), "real deck/runbook sources, materials_md or candidate not all present")
class RealBuildIntegrationTests(unittest.TestCase):
    def test_real_build_into_temp_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            outs = {"deck": Path(tmp) / "facilitator-deck.html", "runbook": Path(tmp) / "runbook.html"}
            with mock.patch("sys.stdout", new=io.StringIO()):
                self.assertEqual(bm.run(out_paths=outs), 0)
                self.assertEqual(bm.run(check=True, out_paths=outs), 0)  # deterministic rebuild
            deck = outs["deck"].read_text(encoding="utf-8")
            runbook = outs["runbook"].read_text(encoding="utf-8")
        groups = bm.load_codes(bm.MATERIALS)
        for placeholder in ("{{NAV}}", "{{PAGES}}", "{{DATA}}", "{{BUILD_INFO}}"):
            self.assertNotIn(placeholder, runbook)
        for placeholder in ("{{SLIDES}}", "{{CODES_JSON}}", "{{BUILD_INFO}}"):
            self.assertNotIn(placeholder, deck)
        for g in groups:
            self.assertIn(g["code"], deck)
        self.assertEqual(bm.check_codes(runbook, groups), [])
        data = json.loads(re.search(r'<script id="rb-data" type="application/json">(.*?)</script>', runbook,
                                    re.S).group(1))
        self.assertEqual(data["build"]["source_candidate"], bm.CANDIDATE_ID)
        evidence = json.loads((bm.CANDIDATE / "build-evidence.json").read_text(encoding="utf-8"))
        zip_sha = {p["id"]: p["zip_sha256"] for p in evidence["packages"]}
        page_ids = {p["id"] for p in data["pages"]}
        decoded_all = {}
        for group in data["groups"]:
            code = next(g["code"] for g in groups if g["id"] == group["id"])
            decoded = bm.decode_payload(group["id"], code.lower(), group["payload"], group["verifier"])
            self.assertEqual(sorted(decoded["pages"]), sorted(group["pages"]))
            decoded_all.update(decoded["pages"])
            for dl_id, b64 in decoded["downloads"].items():
                digest = hashlib.sha256(base64.b64decode(b64)).hexdigest()
                self.assertIn(digest, zip_sha.values(), dl_id)
        # Every in-page xref points at an existing page.
        for markup in list(decoded_all.values()) + [runbook]:
            for target in re.findall(r'href="#p-([a-z0-9-]+)"', markup):
                self.assertIn(target, page_ids)
        hits = bm.scan_forbidden(decoded_all, exemptions=bm.MARKER_EXEMPTIONS)
        self.assertEqual(hits, [])


# ---------------------------------------------------------------- editions

DLC_PLAN = (("intro", 0, 7, "Intro"), ("greenfield", 7, 44, "Domain"), ("b1", 44, 180, "Model"))


class EditionTests(FixtureCase):
    def edition(self, **kw):
        return bm.Edition(**{"name": "dlc", "materials": self.fx.materials, "candidate_id": "candidate",
                             "candidate_root": self.fx.root, "plan": DLC_PLAN, "total_minutes": 180,
                             "storage_prefix": "stwdlc:", **kw})

    def use_dlc_sources(self):
        slides = (slide("intro", "Intro", ' data-minute="00"') +
                  slide("greenfield", "Unlock", ' data-minute="07" data-unlock="greenfield"') +
                  slide("b1", "Unlock B1", ' data-minute="44" data-unlock="b1"') +
                  slide("reveal", "Reveal", ' data-reveal-of="b1"'))
        (self.fx.materials / "facilitator-deck" / "src" / "slides" / "10-all.html").write_text(slides, encoding="utf-8")
        tpl = self.fx.materials / "participant-runbook" / "template"
        (tpl / "runbook.template.html").write_text(
            "<html><script>localStorage.getItem('{{STORAGE_PREFIX}}theme')</script><style>{{STYLE}}</style>"
            "<aside>{{NAV}}<div>{{BUILD_INFO}}</div></aside><main>{{PAGES}}</main>{{DATA}}<script>{{SCRIPT}}</script>"
            "</html>\n", encoding="utf-8")
        (tpl / "runbook.js").write_text("store.set('{{STORAGE_PREFIX}}form:' + id);\n", encoding="utf-8")

    def test_main_defaults_unchanged(self):
        main = bm.load_edition("main")
        self.assertIs(main, bm.MAIN)
        self.assertEqual((main.materials, main.candidate_dir, main.plan, main.segments, main.total_minutes),
                         (bm.MATERIALS, bm.CANDIDATE, bm.PLAN, bm.SEGMENTS, 90))
        self.assertEqual((main.storage_prefix, main.recovery_groups, main.marker_exemptions),
                         ("stw:", bm.RECOVERY_GROUPS, bm.MARKER_EXEMPTIONS))
        self.assertEqual(main.package_output, "dist/materials/participant-materials.zip")
        with self.assertRaises(bm.BuildError):
            bm.load_edition("nope")

    def test_dlc_edition_json(self):
        with mock.patch.object(bm, "DLC_MATERIALS", self.fx.root / "materials-dlc"):
            with self.assertRaises(bm.BuildError) as cm:
                bm.load_edition("dlc")
            self.assertIn("edition.json", str(cm.exception))
            (self.fx.root / "materials-dlc").mkdir()
            (self.fx.root / "materials-dlc" / "edition.json").write_text(json.dumps(
                {"candidate_id": "abc", "total_minutes": 180, "plan": [list(p) for p in DLC_PLAN]}), encoding="utf-8")
            dlc = bm.load_edition("dlc")
        self.assertEqual((dlc.plan, dlc.total_minutes, dlc.storage_prefix), (DLC_PLAN, 180, "stwdlc:"))
        self.assertEqual(dlc.candidate_dir, bm.ROOT / "dist" / "dlc-candidate" / "abc")
        self.assertEqual(dlc.segments, ("intro", "greenfield", "b1", "reveal"))
        self.assertEqual((dlc.recovery_downloads, dlc.b0_guard), ({}, False))
        self.assertNotEqual(dlc.package_output, bm.MAIN.package_output)

    def test_plan_uses_edition_total(self):
        self.assertEqual(bm.plan_problems(DLC_PLAN, 180), [])
        self.assertTrue(any("total 90" in p for p in bm.plan_problems(DLC_PLAN)))
        with self.assertRaises(bm.BuildError):
            bm.validate_slides(good_slides(), GROUPS, edition=self.edition())  # main segments under a dlc plan

    def test_dlc_fixture_build(self):
        self.use_dlc_sources()
        ed = self.edition()
        deck, summary = bm.build_deck(edition=ed)
        self.assertEqual(summary["unlock_slides"], 2)
        out, _ = bm.build_runbook(edition=ed)
        text = out.decode("utf-8")
        self.assertIn("'stwdlc:theme'", text)
        self.assertIn("'stwdlc:form:'", text)
        self.assertNotIn("STORAGE_PREFIX", text)
        self.assertIn('"source_candidate":"candidate"', text)
        # A runbook.js copied without the token would share main's keys: rejected.
        (self.fx.materials / "participant-runbook" / "template" / "runbook.js").write_text(
            "store.get('stw:form:x');\n", encoding="utf-8")
        with self.assertRaises(bm.BuildError):
            bm.build_runbook(edition=ed)
        # The deck's own JS PLAN must match the edition plan.
        (self.fx.materials / "facilitator-deck" / "src" / "js" / "10-core.js").write_text(
            'var PLAN = [{ seg: "intro", label: "Intro", start: 0, end: 7 }];\n', encoding="utf-8")
        with self.assertRaises(bm.BuildError) as cm:
            bm.build_deck(edition=ed)
        self.assertIn("deck js PLAN", str(cm.exception))

    def test_main_js_plan_matches(self):
        script = "\n".join(p.read_text(encoding="utf-8") for p in bm.deck_sources(bm.MATERIALS)["scripts"])
        self.assertTrue(bm.JS_PLAN_ROW.findall(script))
        self.assertEqual(bm.js_plan_problems(script, bm.PLAN), [])

    def test_dlc_js_plan_matches(self):
        # js_plan_problems passes silently when no JS PLAN row parses; pin that the real DLC deck does parse.
        dlc = bm.load_edition("dlc")
        script = "\n".join(p.read_text(encoding="utf-8") for p in bm.deck_sources(dlc.materials)["scripts"])
        self.assertEqual(len(bm.JS_PLAN_ROW.findall(script)), len(dlc.plan))
        self.assertEqual(bm.js_plan_problems(script, dlc.plan), [])
