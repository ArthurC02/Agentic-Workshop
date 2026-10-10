"""Deterministic Markdown renderer for the participant runbook (stdlib only).

Implements the CommonMark-ish subset and the runbook extension blocks defined in
Component Spec v2, section A3 (cmd, callout, include, download, form, gate).
All text is HTML-escaped; raw HTML is never passed through.
"""
from __future__ import annotations

import html
import json
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Callable
from urllib.parse import urlsplit

__all__ = [
    "MarkdownError",
    "RenderContext",
    "parse_front_matter",
    "render_markdown",
    "make_gate_def",
]


class MarkdownError(ValueError):
    """Malformed extension block, bad callout kind, invalid form JSON, external URL, ..."""


@dataclass
class RenderContext:
    page_id: str
    resolve_link: Callable[[str, "str | None"], "str | None"]
    load_include: Callable[[str, str], str]
    register_download: Callable[[str, str, str], dict]
    task_counter: int = 0  # incremented per task-list item (across includes)
    heading_counter: int = 0  # incremented per heading (across includes)
    include_stack: list = field(default_factory=list)  # (zip, path) chain for cycle detection


MAX_INCLUDE_DEPTH = 8
# Source documents open with "> 讀者：… 使用時機：… 前置條件：…" right under the title; that
# authoring metadata is noise for learners, so includes drop it (page and copy/export alike).
READER_NOTE_RE = re.compile(r"\A(\ufeff?#[^\n]*?(\r?\n))(?:[ \t]*\r?\n)*>[ \t]*(?:目標)?讀者：[^\n]*\n(?:>[^\n]*\n)*(?:[ \t]*\r?\n)*")
CALLOUT_KINDS = ("info", "tip", "warning", "danger")
EXTENSIONS = ("cmd", "callout", "include", "download", "form", "gate", "exportall")
FIELD_TYPES = ("text", "textarea", "select", "checkbox", "checklist")
FORM_KEYS = {"id", "title", "kind", "fields"}
FIELD_KEYS = {"id", "label", "type", "options", "items", "hint", "value", "readonly", "suggestions"}
LOCAL_HOSTS = ("127.0.0.1", "localhost")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
_BOM = chr(0xFEFF)
_REPLACEMENT = chr(0xFFFD)
_HARD_BREAK = chr(1)  # internal marker for hard line breaks inside paragraph text


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


# --------------------------------------------------------------------------- front matter

def parse_front_matter(text: str) -> tuple[dict, str]:
    """Parse simple ``key: value`` lines between leading ``---`` lines.

    Returns (meta, body). Text without a leading ``---`` line yields ({}, text).
    """
    text = _normalize_newlines(text)
    if text.startswith(_BOM):
        text = text[1:]
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    meta: dict = {}
    for idx in range(1, len(lines)):
        line = lines[idx]
        if line.strip() == "---":
            return meta, "\n".join(lines[idx + 1:])
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        key = key.strip()
        if not sep or not key:
            raise MarkdownError(f"front matter line {idx + 1}: expected 'key: value', got {line!r}")
        if key in meta:
            raise MarkdownError(f"front matter: duplicate key {key!r}")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        meta[key] = value
    raise MarkdownError("front matter: missing closing '---' line")


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _prepare_lines(md: str) -> list[str]:
    md = _normalize_newlines(md).replace(chr(0), _REPLACEMENT).replace(chr(1), _REPLACEMENT)
    if md.startswith(_BOM):
        md = md[1:]
    out = []
    for line in md.split("\n"):
        stripped = line.lstrip(" \t")
        lead = line[: len(line) - len(stripped)]
        if "\t" in lead:
            lead = lead.expandtabs(4)
        out.append(lead + stripped)
    return out


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _is_blank(line: str) -> bool:
    return not line.strip()


# --------------------------------------------------------------------------- gate / form defs

def make_gate_def(gate_id: str) -> dict:
    """Builder-generated form definition for a ```gate block (spec A3)."""
    if not isinstance(gate_id, str) or not ID_RE.match(gate_id):
        raise MarkdownError(f"gate: invalid id {gate_id!r}")
    upper = gate_id.upper()
    return {
        "id": gate_id,
        "title": f"Gate 核准決策 · {upper}",
        "kind": "gate",
        "fields": [
            {"id": "gate_id", "label": "Gate 編號", "type": "text", "value": upper, "readonly": True},
            {"id": "decision", "label": "決策", "type": "select",
             "options": ["核准（APPROVE）", "有條件核准（APPROVE WITH CONDITIONS）", "退回修正（REJECT AND REVISE）"]},
            {"id": "evidence", "label": "已審查的證據", "type": "textarea",
             "suggestions": [{"label": "證據範本", "text": "Diff：〈檔案〉\n測試：〈指令與結果〉\n文件：〈路徑〉"},
                             {"label": "測試輸出", "text": "pytest -q：〈數字〉 passed、〈數字〉 failed"}]},
            {"id": "conditions", "label": "條件／必要修正", "type": "textarea",
             "suggestions": [{"label": "條件範本", "text": "續行前必須：〈條件〉"},
                             {"label": "修正範本", "text": "退回修正：〈問題〉，補上〈證據／測試〉後再送審"}, "無"]},
            {"id": "approver", "label": "核准人", "type": "text"},
            {"id": "timestamp", "label": "時間／工作坊分鐘", "type": "text",
             "suggestions": [{"label": "分鐘範本", "text": "第 〈分〉 分鐘"}]},
        ],
    }


def _validate_form(obj) -> dict:
    if not isinstance(obj, dict):
        raise MarkdownError("form: definition must be a JSON object")
    extra = set(obj) - FORM_KEYS
    if extra:
        raise MarkdownError(f"form: unknown keys {sorted(extra)}")
    fid = obj.get("id")
    if not isinstance(fid, str) or not ID_RE.match(fid):
        raise MarkdownError(f"form: missing or invalid 'id' ({fid!r})")
    title = obj.get("title")
    if not isinstance(title, str) or not title.strip():
        raise MarkdownError(f"form {fid}: missing or empty 'title'")
    if "kind" in obj and not isinstance(obj["kind"], str):
        raise MarkdownError(f"form {fid}: 'kind' must be a string")
    fields = obj.get("fields")
    if not isinstance(fields, list) or not fields:
        raise MarkdownError(f"form {fid}: 'fields' must be a non-empty list")
    seen = set()
    for pos, fdef in enumerate(fields, 1):
        where = f"form {fid} field #{pos}"
        if not isinstance(fdef, dict):
            raise MarkdownError(f"{where}: must be an object")
        extra = set(fdef) - FIELD_KEYS
        if extra:
            raise MarkdownError(f"{where}: unknown keys {sorted(extra)}")
        for key in ("id", "label", "type"):
            if not isinstance(fdef.get(key), str) or not fdef[key].strip():
                raise MarkdownError(f"{where}: missing or empty {key!r}")
        if fdef["id"] in seen:
            raise MarkdownError(f"{where}: duplicate field id {fdef['id']!r}")
        seen.add(fdef["id"])
        ftype = fdef["type"]
        if ftype not in FIELD_TYPES:
            raise MarkdownError(f"{where}: unknown type {ftype!r}")
        for key, need in (("options", ftype == "select"), ("items", ftype == "checklist")):
            if key in fdef or need:
                val = fdef.get(key)
                if not isinstance(val, list) or not val or not all(isinstance(v, str) for v in val):
                    raise MarkdownError(f"{where}: {key!r} must be a non-empty list of strings")
        if "hint" in fdef and not isinstance(fdef["hint"], str):
            raise MarkdownError(f"{where}: 'hint' must be a string")
        if "readonly" in fdef and not isinstance(fdef["readonly"], bool):
            raise MarkdownError(f"{where}: 'readonly' must be a boolean")
        if "value" in fdef and not isinstance(fdef["value"], (str, bool, list)):
            raise MarkdownError(f"{where}: 'value' must be a string, boolean or list")
        if "suggestions" in fdef:
            # Capsule buttons that insert preset text: "text" or {"label": ..., "text": ...}.
            sug = fdef["suggestions"]
            ok = isinstance(sug, list) and sug and ftype in ("text", "textarea") and all(
                (isinstance(s, str) and s.strip()) or (
                    isinstance(s, dict) and set(s) == {"label", "text"}
                    and all(isinstance(v, str) and v.strip() for v in s.values()))
                for s in sug)
            if not ok:
                raise MarkdownError(f"{where}: 'suggestions' must be a non-empty list of strings or "
                                    "{{label, text}} objects on a text/textarea field")
    return obj


def _form_html(obj: dict) -> str:
    data = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return (f'<div class="rb-form" data-form-id="{_esc(obj["id"])}">'
            f'<script type="application/json" class="rb-form-def">{data}</script></div>')


# --------------------------------------------------------------------------- inline

_ASCII_PUNCT = frozenset("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
_INLINE_SPECIAL = frozenset("\\`[!*\n" + _HARD_BREAK)
_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_TAG_RE = re.compile(r"<[^>]*>")


def _is_punct(ch: str) -> bool:
    if not ch:
        return False
    if ch in _ASCII_PUNCT:
        return True
    return unicodedata.category(ch)[0] in "PS"


def _is_ws(ch: str) -> bool:
    return ch == "" or ch == _HARD_BREAK or ch.isspace()


class _Delim:
    __slots__ = ("count", "orig", "can_open", "can_close", "active", "open_tags", "close_tags")

    def __init__(self, count, can_open, can_close):
        self.count = count
        self.orig = count
        self.can_open = can_open
        self.can_close = can_close
        self.active = True
        self.open_tags: list[str] = []
        self.close_tags: list[str] = []

    def render(self) -> str:
        return "".join(self.close_tags) + "*" * self.count + "".join(reversed(self.open_tags))


def _find_code_close(text: str, start: int, n: int) -> int:
    """Index of a closing backtick run of exactly n backticks at/after start, or -1."""
    j = start
    while True:
        j = text.find("`", j)
        if j < 0:
            return -1
        k = j
        while k < len(text) and text[k] == "`":
            k += 1
        if k - j == n:
            return j
        j = k


def _parse_link_tail(text: str, i: int):
    """Parse '[label](dest "title")' starting at text[i] == '['.

    Returns (label_raw, dest, end_index) or None.
    """
    depth = 0
    j = i
    n = len(text)
    close = -1
    while j < n:
        ch = text[j]
        if ch == "\\" and j + 1 < n:
            j += 2
            continue
        if ch == "`":
            run = j
            while run < n and text[run] == "`":
                run += 1
            end = _find_code_close(text, run, run - j)
            j = end + (run - j) if end >= 0 else run
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                close = j
                break
        j += 1
    if close < 0 or close + 1 >= n or text[close + 1] != "(":
        return None
    k = close + 2
    while k < n and text[k] in " \n":
        k += 1
    if k < n and text[k] == "<":
        end = text.find(">", k + 1)
        if end < 0 or "\n" in text[k + 1:end]:
            return None
        dest = text[k + 1:end]
        k = end + 1
    else:
        start = k
        parens = 0
        while k < n:
            ch = text[k]
            if ch == "\\" and k + 1 < n:
                k += 2
                continue
            if ch.isspace() or ch == _HARD_BREAK:
                break
            if ch == "(":
                parens += 1
            elif ch == ")":
                if parens == 0:
                    break
                parens -= 1
            k += 1
        dest = text[start:k]
    while k < n and text[k] in " \n":
        k += 1
    if k < n and text[k] in "\"'(":
        closer = ")" if text[k] == "(" else text[k]
        end = text.find(closer, k + 1)
        if end < 0:
            return None
        k = end + 1
        while k < n and text[k] in " \n":
            k += 1
    if k >= n or text[k] != ")":
        return None
    dest = re.sub(r"\\([!-/:-@\[-`{-~])", r"\1", dest)
    return text[i + 1:close], dest, k + 1


class _InlineRenderer:
    def __init__(self, ctx: RenderContext, source):
        self.ctx = ctx
        self.source = source

    def render(self, text: str, allow_links: bool = True) -> str:
        nodes: list = []
        delims: list[_Delim] = []
        buf: list[str] = []
        i = 0
        n = len(text)

        def flush():
            if buf:
                nodes.append(_esc("".join(buf)))
                buf.clear()

        while i < n:
            ch = text[i]
            if ch not in _INLINE_SPECIAL:
                buf.append(ch)
                i += 1
                continue
            if ch == "\\":
                nxt = text[i + 1] if i + 1 < n else ""
                if nxt and nxt in _ASCII_PUNCT:
                    buf.append(nxt)
                    i += 2
                else:
                    buf.append("\\")
                    i += 1
                continue
            if ch == "\n":
                buf.append("\n")
                i += 1
                continue
            if ch == _HARD_BREAK:
                flush()
                nodes.append("<br>\n")
                i += 1
                continue
            if ch == "`":
                run = i
                while run < n and text[run] == "`":
                    run += 1
                width = run - i
                end = _find_code_close(text, run, width)
                if end < 0:
                    buf.append("`" * width)
                    i = run
                    continue
                code = text[run:end].replace("\n", " ").replace(_HARD_BREAK, " ")
                if len(code) >= 2 and code[0] == " " and code[-1] == " " and code.strip(" "):
                    code = code[1:-1]
                flush()
                nodes.append("<code>" + _esc(code) + "</code>")
                i = end + width
                continue
            if ch == "!" and i + 1 < n and text[i + 1] == "[" and _parse_link_tail(text, i + 1):
                raise MarkdownError(f"images are not supported: {text[i:i + 60]!r}")
            if ch == "[" and allow_links:
                parsed = _parse_link_tail(text, i)
                if parsed:
                    label, dest, end = parsed
                    flush()
                    nodes.append(self._link(label, dest))
                    i = end
                    continue
            if ch == "*":
                run = i
                while run < n and text[run] == "*":
                    run += 1
                before = text[i - 1] if i > 0 else ""
                after = text[run] if run < n else ""
                left = not _is_ws(after) and (not _is_punct(after) or _is_ws(before) or _is_punct(before))
                right = not _is_ws(before) and (not _is_punct(before) or _is_ws(after) or _is_punct(after))
                flush()
                delim = _Delim(run - i, left, right)
                nodes.append(delim)
                delims.append(delim)
                i = run
                continue
            buf.append(ch)
            i += 1
        flush()
        _process_emphasis(delims)
        return "".join(node.render() if isinstance(node, _Delim) else node for node in nodes)

    def _link(self, label: str, dest: str) -> str:
        href = dest.strip()
        label_html = self.render(label, allow_links=False)
        if _SCHEME_RE.match(href) or href.startswith("//"):
            parts = urlsplit("http:" + href if href.startswith("//") else href)
            try:
                host = (parts.hostname or "").lower()
            except ValueError:
                host = ""
            if parts.scheme.lower() in ("http", "https") and host in LOCAL_HOSTS:
                return "<code>" + _TAG_RE.sub("", label_html) + "</code>"
            raise MarkdownError(f"external link not allowed: {href!r}")
        path = href.split("#", 1)[0].split("?", 1)[0]
        if href.startswith("#") or path.lower().endswith(".md"):
            target = self.ctx.resolve_link(href, self.source)
            if target is None:
                return label_html
            return f'<a class="rb-xref" href="{_esc(str(target))}">{label_html}</a>'
        return label_html


def _process_emphasis(delims: list[_Delim]) -> None:
    """CommonMark 'process emphasis' for '*' runs (strong for pairs, em for singles)."""
    for ci, closer in enumerate(delims):
        if not closer.can_close:
            continue
        while closer.active and closer.count > 0:
            oi = ci - 1
            opener = None
            while oi >= 0:
                cand = delims[oi]
                if cand.active and cand.count > 0 and cand.can_open:
                    rule_of_three = (cand.can_close or closer.can_open) \
                        and (cand.orig + closer.orig) % 3 == 0 \
                        and not (cand.orig % 3 == 0 and closer.orig % 3 == 0)
                    if not rule_of_three:
                        opener = cand
                        break
                oi -= 1
            if opener is None:
                break
            use = 2 if opener.count >= 2 and closer.count >= 2 else 1
            tag = "strong" if use == 2 else "em"
            opener.count -= use
            closer.count -= use
            opener.open_tags.append(f"<{tag}>")
            closer.close_tags.append(f"</{tag}>")
            for mid in delims[oi + 1:ci]:
                mid.active = False


# --------------------------------------------------------------------------- block helpers

_FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")
_ATX_RE = re.compile(r"^ {0,3}(#{1,6})(?=[ \t]|$)(.*)$")
_HR_RE = re.compile(r"^ {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$")
_BQ_RE = re.compile(r"^ {0,3}>( ?)(.*)$")
_LIST_RE = re.compile(r"^( {0,3})([-*+]|\d{1,9}[.)])(?:([ \t]+)(.*))?$")
_LIST_ANY_RE = re.compile(r"^( *)([-*+]|\d{1,9}[.)])(?:[ \t]+|$)")
_TASK_RE = re.compile(r"^\[([ xX])\](?:[ \t]+(.*)|$)")
_TDELIM_CELL_RE = re.compile(r"^:?-+:?$")
_KV_KEY_RE = re.compile(r"([a-z_]+)=")


def _fence_open(line: str):
    """Return (indent, char, width, info) for an opening code fence, else None."""
    m = _FENCE_RE.match(line)
    if not m:
        return None
    fence = m.group(2)
    info = m.group(3)
    if fence[0] == "`" and "`" in info:
        return None
    return len(m.group(1)), fence[0], len(fence), info.strip()


def _is_fence_close(line: str, char: str, width: int) -> bool:
    m = re.match(r"^ {0,3}(" + re.escape(char) + r"{%d,})[ \t]*$" % width, line)
    return m is not None


def _split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells: list[str] = []
    cur: list[str] = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "|":
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    cells.append("".join(cur).strip())
    return cells


def _table_aligns(line: str):
    """Alignment list for a GFM delimiter row, or None if not a delimiter row."""
    if "|" not in line or not line.strip():
        return None
    cells = _split_row(line)
    aligns = []
    for cell in cells:
        if not _TDELIM_CELL_RE.match(cell):
            return None
        if cell.startswith(":") and cell.endswith(":"):
            aligns.append("center")
        elif cell.endswith(":"):
            aligns.append("right")
        elif cell.startswith(":"):
            aligns.append("left")
        else:
            aligns.append(None)
    return aligns


def _table_start(lines: list[str], i: int):
    """Return alignments if lines[i] is a table header followed by a matching delimiter row."""
    if i + 1 >= len(lines) or "|" not in lines[i] or _indent(lines[i]) > 3:
        return None
    aligns = _table_aligns(lines[i + 1])
    if aligns is None or len(_split_row(lines[i])) != len(aligns):
        return None
    return aligns


def _list_marker(line: str):
    """(indent, marker, spaces, rest) for a list item line with <=3 indent, else None."""
    if _HR_RE.match(line):
        return None
    m = _LIST_RE.match(line)
    if not m:
        return None
    return len(m.group(1)), m.group(2), m.group(3) or "", m.group(4) or ""


def _list_kind(marker: str) -> tuple[bool, str]:
    return (marker[0].isdigit(), marker[-1])


def _parse_kv(line: str, keys: tuple[str, ...], where: str, rest_key: str | None = None) -> dict:
    result: dict = {}
    s = line.strip()
    while s:
        m = _KV_KEY_RE.match(s)
        if not m:
            raise MarkdownError(f"{where}: expected key=value, got {s!r}")
        key = m.group(1)
        s = s[m.end():]
        if key not in keys:
            raise MarkdownError(f"{where}: unknown key {key!r}")
        if key in result:
            raise MarkdownError(f"{where}: duplicate key {key!r}")
        if key == rest_key:
            value, s = s.strip(), ""
        else:
            value, _, s = s.partition(" ")
            s = s.lstrip()
        if not value:
            raise MarkdownError(f"{where}: empty value for {key!r}")
        result[key] = value
    missing = [k for k in keys if k not in result]
    if missing:
        raise MarkdownError(f"{where}: missing keys {missing}")
    return result


def _single_line(body: list[str], where: str) -> str:
    content = [line for line in body if line.strip()]
    if len(content) != 1:
        raise MarkdownError(f"{where}: expected exactly one key=value line, got {len(content)}")
    return content[0]


def _trim_blank(lines: list[str]) -> list[str]:
    start, end = 0, len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def _code_pre(code: str, lang: str, shell: str | None = None) -> str:
    attrs = f' data-lang="{_esc(lang or "text")}"'
    if shell:
        attrs += f' data-shell="{_esc(shell)}"'
    return f'<pre class="rb-code"{attrs}><code>{_esc(code)}</code></pre>'


def _join_paragraph(lines: list[str]) -> str:
    parts = []
    last = len(lines) - 1
    for idx, line in enumerate(lines):
        if idx == last:
            parts.append(line.rstrip(" \t"))
            break
        trailing = len(line) - len(line.rstrip("\\"))
        if trailing % 2 == 1:
            parts.append(line[:-1] + _HARD_BREAK)
        elif line.endswith("  "):
            parts.append(line.rstrip(" \t") + _HARD_BREAK)
        else:
            parts.append(line.rstrip(" \t") + "\n")
    return "".join(parts)


# --------------------------------------------------------------------------- block parser

class _BlockParser:
    def __init__(self, ctx: RenderContext, shift: int, source):
        self.ctx = ctx
        self.shift = shift
        self.source = source
        self.inline = _InlineRenderer(ctx, source)

    # Each block is ("p", inline_html) or ("html", html).
    def parse(self, lines: list[str]) -> list[tuple[str, str]]:
        blocks: list[tuple[str, str]] = []
        i = 0
        n = len(lines)
        while i < n:
            line = lines[i]
            if _is_blank(line):
                i += 1
                continue
            fence = _fence_open(line)
            if fence:
                i = self._fence(lines, i, fence, blocks)
                continue
            m = _ATX_RE.match(line)
            if m:
                blocks.append(("html", self._heading(len(m.group(1)), m.group(2))))
                i += 1
                continue
            if _HR_RE.match(line):
                blocks.append(("html", "<hr>"))
                i += 1
                continue
            if _BQ_RE.match(line):
                i = self._blockquote(lines, i, blocks)
                continue
            if _list_marker(line):
                i = self._list(lines, i, blocks)
                continue
            aligns = _table_start(lines, i)
            if aligns is not None:
                i = self._table(lines, i, aligns, blocks)
                continue
            i = self._paragraph(lines, i, blocks)
        return blocks

    def _interrupts(self, lines: list[str], i: int) -> bool:
        line = lines[i]
        if _is_blank(line) or _fence_open(line) or _ATX_RE.match(line) or _HR_RE.match(line):
            return True
        if _BQ_RE.match(line):
            return True
        marker = _list_marker(line)
        if marker and marker[3].strip():
            return True
        return _table_start(lines, i) is not None

    def _paragraph(self, lines, i, blocks) -> int:
        para = [lines[i].lstrip(" ")]
        i += 1
        while i < len(lines) and not self._interrupts(lines, i):
            para.append(lines[i].lstrip(" "))
            i += 1
        blocks.append(("p", self.inline.render(_join_paragraph(para))))
        return i

    def _heading(self, hashes: int, raw: str) -> str:
        text = raw.strip()
        text = re.sub(r"(?:^|[ \t]+)#+$", "", text).strip()
        level = min(6, hashes + self.shift)
        self.ctx.heading_counter += 1
        hid = f"{self.ctx.page_id}--h{self.ctx.heading_counter}"
        return f'<h{level} id="{_esc(hid)}">{self.inline.render(text)}</h{level}>'

    def _blockquote(self, lines, i, blocks) -> int:
        inner: list[str] = []
        while i < len(lines):
            line = lines[i]
            m = _BQ_RE.match(line)
            if m:
                inner.append(m.group(2))
            elif inner and inner[-1].strip() and not self._interrupts(lines, i):
                inner.append(line)  # lazy paragraph continuation
            else:
                break
            i += 1
        body = "\n".join(_render_blocks(self.parse(inner)))
        blocks.append(("html", "<blockquote>\n" + body + "\n</blockquote>" if body else "<blockquote></blockquote>"))
        return i

    def _list(self, lines, i, blocks) -> int:
        n = len(lines)
        first = _list_marker(lines[i])
        kind = _list_kind(first[1])
        ordered = kind[0]
        start = int(first[1][:-1]) if ordered else 1
        items: list[list[str]] = []
        loose = False
        while i < n:
            marker = _list_marker(lines[i])
            if not marker or _list_kind(marker[1]) != kind:
                break
            m_indent, mark, spaces, rest = marker
            if not rest:
                content_indent = m_indent + len(mark) + 1
            elif len(spaces) > 4:
                content_indent = m_indent + len(mark) + 1
                rest = spaces[1:] + rest
            else:
                content_indent = m_indent + len(mark) + len(spaces)
            item = [rest]
            i += 1
            while i < n:
                line = lines[i]
                if _is_blank(line):
                    item.append("")
                    i += 1
                    continue
                ind = _indent(line)
                if ind >= content_indent:
                    item.append(line[content_indent:])
                elif _LIST_ANY_RE.match(line) and not _HR_RE.match(line) and ind >= m_indent + 2:
                    item.append(line[ind:])
                elif item[-1].strip() and not self._interrupts(lines, i):
                    item.append(line.lstrip(" "))  # lazy continuation
                else:
                    break
                i += 1
            trailing = 0
            while item and not item[-1].strip():
                item.pop()
                trailing += 1
            for pos in range(1, len(item)):
                if not item[pos - 1].strip() and item[pos].strip() and not item[pos].startswith(" ") \
                        and not _LIST_ANY_RE.match(item[pos]):
                    loose = True
            items.append(item)
            if trailing:
                nxt = _list_marker(lines[i]) if i < n else None
                if nxt and _list_kind(nxt[1]) == kind:
                    loose = True
                else:
                    break
        blocks.append(("html", self._render_list(items, ordered, start, loose)))
        return i

    def _render_list(self, items, ordered, start, loose) -> str:
        out_items = []
        has_task = False
        for item in items:
            task_no = None
            if not ordered:
                tm = _TASK_RE.match(item[0])
                if tm:
                    self.ctx.task_counter += 1
                    task_no = self.ctx.task_counter
                    item = [tm.group(2) or ""] + item[1:]
                    has_task = True
            parts = self.parse(item)
            if task_no is not None:
                span = ""
                if parts and parts[0][0] == "p":
                    span = parts[0][1]
                    parts = parts[1:]
                check = f"{self.ctx.page_id}:{task_no}"
                head = (f'<label><input type="checkbox" class="rb-check" data-check="{_esc(check)}">'
                        f"<span>{span}</span></label>")
                rest = _render_blocks(parts, tight=not loose)
                out_items.append('<li class="rb-task">' + "\n".join([head] + rest) + "</li>")
            else:
                out_items.append("<li>" + "\n".join(_render_blocks(parts, tight=not loose)) + "</li>")
        if ordered:
            tag = "ol"
            attrs = f' start="{start}"' if start != 1 else ""
        else:
            tag = "ul"
            attrs = ' class="rb-tasks"' if has_task else ""
        return f"<{tag}{attrs}>\n" + "\n".join(out_items) + f"\n</{tag}>"

    def _table(self, lines, i, aligns, blocks) -> int:
        header = _split_row(lines[i])
        i += 2
        rows = []
        while i < len(lines):
            line = lines[i]
            if _is_blank(line) or _fence_open(line) or _ATX_RE.match(line) or _BQ_RE.match(line) \
                    or _HR_RE.match(line) or _list_marker(line):
                break
            rows.append(_split_row(line))
            i += 1

        def cell(tag, text, align, label=""):
            style = f' style="text-align:{align}"' if align else ""
            return f"<{tag}{style}{label}>{self.inline.render(text)}</{tag}>"

        width = len(aligns)
        # 3+ columns: each <td> carries its header as data-label so phones can show rows as cards.
        stack = width >= 3
        labels = [""] * width
        if stack:
            labels = [' data-label="' + html.escape(html.unescape(re.sub(r"<[^>]+>", "", self.inline.render(
                header[c] if c < len(header) else ""))).strip(), quote=True) + '"' for c in range(width)]
        cls = "rb-table rb-table-stack" if stack else "rb-table"
        out = [f'<div class="rb-table-wrap"><table class="{cls}">', "<thead>", "<tr>"]
        out += [cell("th", header[c], aligns[c]) for c in range(width)]
        out += ["</tr>", "</thead>", "<tbody>"]
        for row in rows:
            row = (row + [""] * width)[:width]
            out.append("<tr>")
            out += [cell("td", row[c], aligns[c], labels[c]) for c in range(width)]
            out.append("</tr>")
        out += ["</tbody>", "</table></div>"]
        blocks.append(("html", "\n".join(out)))
        return i

    # ------------------------------------------------------------------- fences / extensions

    def _fence(self, lines, i, fence, blocks) -> int:
        indent, char, width, info = fence
        words = info.split()
        lang = words[0] if words else ""
        is_ext = lang in EXTENSIONS
        body: list[str] = []
        j = i + 1
        closed = False
        while j < len(lines):
            if _is_fence_close(lines[j], char, width):
                closed = True
                break
            line = lines[j]
            strip = min(indent, _indent(line))
            body.append(line[strip:])
            j += 1
        if not closed and is_ext:
            raise MarkdownError(f"unclosed ```{lang} block (line {i + 1})")
        end = j + 1 if closed else j
        if not is_ext:
            blocks.append(("html", _code_pre("\n".join(body), lang)))
            return end
        if lang != "callout" and len(words) > 1:
            raise MarkdownError(f"```{lang}: unexpected info string {info!r}")
        handler = getattr(self, "_ext_" + lang)
        blocks.append(("html", handler(words, body)))
        return end

    def _ext_cmd(self, words, body) -> str:
        sections: dict[str, list[str]] = {}
        before: list[str] = []
        current = None
        for line in body:
            mark = line.strip()
            if mark in ("# powershell", "# bash"):
                shell = mark[2:]
                if shell in sections:
                    raise MarkdownError(f"```cmd: duplicate '# {shell}' section")
                sections[shell] = []
                current = shell
                continue
            (before if current is None else sections[current]).append(line)
        if not sections:
            return _code_pre("\n".join(_trim_blank(before)), "text")
        if any(line.strip() for line in before):
            raise MarkdownError("```cmd: text before the first '# powershell' / '# bash' marker")
        missing = [s for s in ("powershell", "bash") if s not in sections]
        if missing:
            raise MarkdownError(f"```cmd: missing section(s) {missing}")
        pres = []
        for shell in ("powershell", "bash"):
            code = _trim_blank(sections[shell])
            if not code:
                raise MarkdownError(f"```cmd: empty '# {shell}' section")
            pres.append(_code_pre("\n".join(code), shell, shell))
        tabs = ('<div class="rb-cmd-tabs" role="tablist">'
                '<button type="button" class="rb-cmd-tab" data-shell="powershell">PowerShell</button>'
                '<button type="button" class="rb-cmd-tab" data-shell="bash">bash</button></div>')
        return '<div class="rb-cmd">' + tabs + "".join(pres) + "</div>"

    def _ext_callout(self, words, body) -> str:
        if len(words) != 2 or words[1] not in CALLOUT_KINDS:
            raise MarkdownError(f"```callout: kind must be one of {list(CALLOUT_KINDS)}, got {words[1:]}")
        kind = words[1]
        content = _trim_blank(body)
        if not content:
            raise MarkdownError(f"```callout {kind}: missing title line")
        title = self.inline.render(content[0].strip())
        inner = "\n".join(_render_blocks(self.parse(content[1:])))
        return (f'<div class="rb-callout rb-callout-{kind}"><div class="rb-callout-title">{title}</div>'
                f'<div class="rb-callout-body">{inner}</div></div>')

    def _ext_include(self, words, body) -> str:
        kv = _parse_kv(_single_line(body, "```include"), ("zip", "path"), "```include")
        zip_name, path = kv["zip"], kv["path"]
        key = (zip_name, path)
        stack = self.ctx.include_stack
        if key in stack:
            raise MarkdownError(f"```include: recursive include of {zip_name}:{path}")
        if len(stack) >= MAX_INCLUDE_DEPTH:
            raise MarkdownError(f"```include: nesting deeper than {MAX_INCLUDE_DEPTH} at {zip_name}:{path}")
        text = self.ctx.load_include(zip_name, path)
        if not isinstance(text, str):
            raise MarkdownError(f"```include: loader returned {type(text).__name__} for {zip_name}:{path}")
        text = READER_NOTE_RE.sub(r"\1\2", text, count=1)
        stack.append(key)
        try:
            inner = render_markdown(text, self.ctx, heading_shift=self.shift, source=path)
        finally:
            stack.pop()
        base = path.rstrip("/").rsplit("/", 1)[-1]
        # Raw Markdown for the copy / download buttons; "</" escaped so it cannot close the script.
        raw = json.dumps(text, ensure_ascii=False).replace("</", "<\\/")
        return (f'<section class="rb-include" data-source="{_esc(zip_name + ":" + path)}">'
                f'<div class="rb-include-meta">來源文件：<code>{_esc(base)}</code>'
                f'<script type="application/json" class="rb-include-src">{raw}</script></div>\n'
                f"{inner}\n</section>")

    def _ext_download(self, words, body) -> str:
        kv = _parse_kv(_single_line(body, "```download"), ("id", "zip", "label"), "```download",
                       rest_key="label")
        did = kv["id"]
        if not ID_RE.match(did):
            raise MarkdownError(f"```download: invalid id {did!r}")
        meta = self.ctx.register_download(did, kv["zip"], kv["label"])
        if not isinstance(meta, dict) or not isinstance(meta.get("size_kb"), int) \
                or isinstance(meta.get("size_kb"), bool) or not isinstance(meta.get("sha12"), str):
            raise MarkdownError(f"```download {did}: register_download must return {{size_kb:int, sha12:str}}")
        return (f'<div class="rb-download-card"><button type="button" class="rb-download" '
                f'data-download="{_esc(did)}" data-filename="{_esc(did)}.zip">{_esc(kv["label"])}</button>'
                f'<span class="rb-download-meta">ZIP · {meta["size_kb"]} KB · SHA256 {_esc(meta["sha12"])}</span></div>')

    def _ext_form(self, words, body) -> str:
        raw = "\n".join(body)
        if not raw.strip():
            raise MarkdownError("```form: empty definition")
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise MarkdownError(f"```form: invalid JSON ({exc})") from None
        return _form_html(_validate_form(obj))

    def _ext_gate(self, words, body) -> str:
        kv = _parse_kv(_single_line(body, "```gate"), ("id",), "```gate")
        return _form_html(make_gate_def(kv["id"]))

    def _ext_exportall(self, words, body) -> str:
        if any(line.strip() for line in body):
            raise MarkdownError("```exportall: takes no content")
        return '<div class="rb-export-all"></div>'


def _render_blocks(blocks: list[tuple[str, str]], tight: bool = False) -> list[str]:
    out = []
    for kind, content in blocks:
        if kind == "p":
            out.append(content if tight else f"<p>{content}</p>")
        else:
            out.append(content)
    return out


# --------------------------------------------------------------------------- entry point

def render_markdown(md: str, ctx: RenderContext, *, heading_shift: int = 1, source: str | None = None) -> str:
    """Render runbook Markdown to HTML (the inner html of .rb-page-body or of an include)."""
    if not isinstance(heading_shift, int) or isinstance(heading_shift, bool) or not 0 <= heading_shift <= 5:
        raise MarkdownError(f"heading_shift must be an int in 0..5, got {heading_shift!r}")
    parser = _BlockParser(ctx, heading_shift, source)
    return "\n".join(_render_blocks(parser.parse(_prepare_lines(md))))
