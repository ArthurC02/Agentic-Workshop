"""Unit tests for materials_md (runbook Markdown renderer, Component Spec v2 section A3)."""
import json
import pathlib
import re
import sys
import unittest
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from materials_md import (  # noqa: E402
    MarkdownError,
    RenderContext,
    make_gate_def,
    parse_front_matter,
    render_markdown,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT / "agentic-workshop" / "materials" / "participant-runbook" / "content"
DIST = ROOT / "dist" / "p11-candidate" / "c02cf8abb06e0155"


class Recorder:
    """Dummy callbacks for RenderContext that record every call."""

    def __init__(self, includes=None, links=None):
        self.includes = includes or {}
        self.links = links  # None -> "#p-<id>" for '#id', None for others
        self.link_calls = []
        self.include_calls = []
        self.download_calls = []

    def resolve(self, href, source):
        self.link_calls.append((href, source))
        if self.links is not None:
            return self.links.get(href)
        return "#p-" + href[1:] if href.startswith("#") else None

    def load(self, zip_name, path):
        self.include_calls.append((zip_name, path))
        return self.includes[(zip_name, path)]

    def register(self, did, zip_name, label):
        self.download_calls.append((did, zip_name, label))
        return {"size_kb": 23, "sha12": "abcdef012345"}

    def ctx(self, page="pg"):
        return RenderContext(page, self.resolve, self.load, self.register)


def render(md, page="pg", rec=None, **kw):
    rec = rec or Recorder()
    return render_markdown(md, rec.ctx(page), **kw)


def fence(kind, *lines):
    return "\n".join(["```" + kind, *lines, "```"])


class FrontMatterTests(unittest.TestCase):
    def test_parses_simple_key_values(self):
        meta, body = parse_front_matter("---\nid: welcome\ntitle: 歡迎: 使用\nminute: '00-07'\n---\n# H\n")
        self.assertEqual(meta, {"id": "welcome", "title": "歡迎: 使用", "minute": "00-07"})
        self.assertEqual(body, "# H\n")

    def test_crlf_and_bom(self):
        meta, body = parse_front_matter("\ufeff---\r\nid: x\r\n---\r\nbody")
        self.assertEqual(meta, {"id": "x"})
        self.assertEqual(body, "body")

    def test_without_front_matter(self):
        self.assertEqual(parse_front_matter("# Title\n"), ({}, "# Title\n"))

    def test_errors(self):
        for text in ("---\nid: x\n", "---\nnot a pair\n---\n", "---\nid: a\nid: b\n---\n"):
            with self.assertRaises(MarkdownError, msg=text):
                parse_front_matter(text)


class HeadingTests(unittest.TestCase):
    def test_shift_and_sequential_ids(self):
        out = render("# A\n\n## B\n### C\n###### F\n", page="welcome")
        self.assertEqual(out, '<h2 id="welcome--h1">A</h2>\n<h3 id="welcome--h2">B</h3>\n'
                              '<h4 id="welcome--h3">C</h4>\n<h6 id="welcome--h4">F</h6>')

    def test_shift_zero_and_closing_hashes(self):
        self.assertEqual(render("## T ##", heading_shift=0), '<h2 id="pg--h1">T</h2>')

    def test_hash_without_space_is_paragraph(self):
        self.assertEqual(render("#tag"), "<p>#tag</p>")

    def test_inline_in_heading_is_rendered_and_escaped(self):
        self.assertEqual(render("# **B** `<x>` <i>"),
                         '<h2 id="pg--h1"><strong>B</strong> <code>&lt;x&gt;</code> &lt;i&gt;</h2>')

    def test_invalid_shift(self):
        for bad in (-1, 6, "1", True):
            with self.assertRaises(MarkdownError):
                render("# x", heading_shift=bad)


class ParagraphInlineTests(unittest.TestCase):
    def test_soft_break_kept(self):
        self.assertEqual(render("a\nb"), "<p>a\nb</p>")

    def test_hard_breaks(self):
        self.assertEqual(render("a  \nb\\\nc"), "<p>a<br>\nb<br>\nc</p>")

    def test_trailing_spaces_on_last_line_dropped(self):
        self.assertEqual(render("a  "), "<p>a</p>")

    def test_emphasis(self):
        self.assertEqual(render("**s** *e* ***both***"),
                         "<p><strong>s</strong> <em>e</em> <em><strong>both</strong></em></p>")

    def test_emphasis_inside_cjk_text(self):
        self.assertEqual(render("請在 **22 分鐘**內完成，**Tool**：好"),
                         "<p>請在 <strong>22 分鐘</strong>內完成，<strong>Tool</strong>：好</p>")

    def test_unmatched_and_spaced_stars_are_literal(self):
        self.assertEqual(render("a * b ** c *d"), "<p>a * b ** c *d</p>")

    def test_nested_emphasis(self):
        self.assertEqual(render("*a **b** c*"), "<p><em>a <strong>b</strong> c</em></p>")

    def test_code_spans(self):
        self.assertEqual(render("`<b>&` `` a`b `` `x"),
                         "<p><code>&lt;b&gt;&amp;</code> <code>a`b</code> `x</p>")

    def test_code_span_keeps_backslashes_and_stars(self):
        self.assertEqual(render(r"`C:\work\*` \*lit\*"), r"<p><code>C:\work\*</code> *lit*</p>")

    def test_backslash_before_non_punct_is_literal(self):
        self.assertEqual(render(r"C:\work\g0"), r"<p>C:\work\g0</p>")

    def test_raw_html_is_escaped(self):
        self.assertEqual(render('<script>alert("x")</script> & \'q\''),
                         "<p>&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt; &amp; &#x27;q&#x27;</p>")

    def test_html_block_is_escaped_not_passed_through(self):
        out = render('<div onclick="x">\n<b>hi</b>\n</div>')
        self.assertNotIn("<div", out)
        self.assertNotIn("<b>", out)
        self.assertIn("&lt;div onclick=&quot;x&quot;&gt;", out)

    def test_horizontal_rules(self):
        self.assertEqual(render("a\n\n---\n\n***\n\n_ _ _"), "<p>a</p>\n<hr>\n<hr>\n<hr>")

    def test_image_is_rejected(self):
        with self.assertRaises(MarkdownError):
            render("![alt](pic.png)")

    def test_deterministic(self):
        md = "# T\n\n- [ ] a\n- [x] b\n\n| a | b |\n|---|:-:|\n| 1 | 2 |\n"
        self.assertEqual(render(md), render(md))


class LinkTests(unittest.TestCase):
    def test_page_anchor_link(self):
        rec = Recorder()
        out = render("見 [環境 **準備**](#environment)。", rec=rec)
        self.assertEqual(out, '<p>見 <a class="rb-xref" href="#p-environment">環境 <strong>準備</strong></a>。</p>')
        self.assertEqual(rec.link_calls, [("#environment", None)])

    def test_relative_md_link_passes_source(self):
        rec = Recorder(links={"02-x.md#escalation": "#p-x"})
        out = render("[X](02-x.md#escalation) [Y](../y.md)", rec=rec, source="a/b/c.md")
        self.assertEqual(out, '<p><a class="rb-xref" href="#p-x">X</a> Y</p>')
        self.assertEqual(rec.link_calls, [("02-x.md#escalation", "a/b/c.md"), ("../y.md", "a/b/c.md")])

    def test_unresolved_link_renders_text_only(self):
        self.assertEqual(render("[gone](#nowhere)", rec=Recorder(links={})), "<p>gone</p>")

    def test_non_md_relative_link_is_text_and_not_resolved(self):
        rec = Recorder()
        self.assertEqual(render("[src](src/app.py)", rec=rec), "<p>src</p>")
        self.assertEqual(rec.link_calls, [])

    def test_resolved_href_is_escaped(self):
        out = render("[a](#a)", rec=Recorder(links={"#a": '#p-"a"'}))
        self.assertEqual(out, '<p><a class="rb-xref" href="#p-&quot;a&quot;">a</a></p>')

    def test_localhost_links_render_as_code(self):
        out = render("[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs) "
                     "[api](https://localhost:8443/x)")
        self.assertEqual(out, "<p><code>http://127.0.0.1:8000/docs</code> <code>api</code></p>")

    def test_external_links_are_errors(self):
        for md in ("[x](https://example.com)", "[x](http://127.0.0.2/)", "[x](mailto:a@b.c)",
                   "[x](javascript:alert(1))", "[x](//evil.example/x.md)"):
            with self.assertRaises(MarkdownError, msg=md):
                render(md)

    def test_bare_url_text_is_not_a_link(self):
        self.assertEqual(render("see https://example.com"), "<p>see https://example.com</p>")

    def test_link_with_title_and_angle_destination(self):
        out = render('[a](<#a> "t") [b](#b \'t\')')
        self.assertEqual(out, '<p><a class="rb-xref" href="#p-a">a</a> <a class="rb-xref" href="#p-b">b</a></p>')

    def test_brackets_without_destination_are_literal(self):
        self.assertEqual(render("[x] and [y] (z)"), "<p>[x] and [y] (z)</p>")


class ListTests(unittest.TestCase):
    def test_tight_bullet_list(self):
        self.assertEqual(render("- a\n- **b**\n* c"), "<ul>\n<li>a</li>\n<li><strong>b</strong></li>\n</ul>\n"
                                                      "<ul>\n<li>c</li>\n</ul>")

    def test_ordered_list_with_start(self):
        self.assertEqual(render("3. a\n4. b"), '<ol start="3">\n<li>a</li>\n<li>b</li>\n</ol>')
        self.assertEqual(render("1. a\n2. b"), "<ol>\n<li>a</li>\n<li>b</li>\n</ol>")

    def test_nested_two_space_indent(self):
        self.assertEqual(render("- a\n  - b\n    - c\n- d"),
                         "<ul>\n<li>a\n<ul>\n<li>b\n<ul>\n<li>c</li>\n</ul></li>\n</ul></li>\n<li>d</li>\n</ul>")

    def test_nested_four_space_indent(self):
        self.assertEqual(render("- a\n    - b\n- c"),
                         "<ul>\n<li>a\n<ul>\n<li>b</li>\n</ul></li>\n<li>c</li>\n</ul>")

    def test_ordered_with_nested_bullets_two_and_three_spaces(self):
        expected = "<ol>\n<li>a\n<ul>\n<li>x</li>\n</ul></li>\n<li>b\n<ul>\n<li>y</li>\n</ul></li>\n</ol>"
        self.assertEqual(render("1. a\n  - x\n2. b\n   - y"), expected)

    def test_loose_list_wraps_paragraphs(self):
        self.assertEqual(render("- a\n\n- b\n\n  more"),
                         "<ul>\n<li><p>a</p></li>\n<li><p>b</p>\n<p>more</p></li>\n</ul>")

    def test_lazy_continuation_and_list_interrupts_paragraph(self):
        self.assertEqual(render("intro\n- a\ncont\n\nafter"),
                         "<p>intro</p>\n<ul>\n<li>a\ncont</li>\n</ul>\n<p>after</p>")

    def test_list_item_with_code_fence(self):
        out = render("- step\n\n  ```bash\n  ls <dir>\n  ```")
        self.assertIn('<pre class="rb-code" data-lang="bash"><code>ls &lt;dir&gt;</code></pre></li>', out)


class TaskListTests(unittest.TestCase):
    def test_task_markup_and_numbering(self):
        out = render("- [ ] one `x`\n- [x] two\n- plain", page="env")
        self.assertEqual(out, '<ul class="rb-tasks">\n'
                              '<li class="rb-task"><label><input type="checkbox" class="rb-check" '
                              'data-check="env:1"><span>one <code>x</code></span></label></li>\n'
                              '<li class="rb-task"><label><input type="checkbox" class="rb-check" '
                              'data-check="env:2"><span>two</span></label></li>\n'
                              "<li>plain</li>\n</ul>")

    def test_numbering_continues_across_lists_and_nesting(self):
        rec = Recorder()
        ctx = rec.ctx("p")
        out = render_markdown("- [ ] a\n  - [ ] b\n\ntext\n\n- [ ] c", ctx)
        self.assertEqual(re.findall(r'data-check="([^"]+)"', out), ["p:1", "p:2", "p:3"])
        self.assertEqual(ctx.task_counter, 3)
        out2 = render_markdown("- [ ] d", ctx)
        self.assertIn('data-check="p:4"', out2)

    def test_ordered_list_brackets_are_text(self):
        self.assertEqual(render("1. [ ] a"), "<ol>\n<li>[ ] a</li>\n</ol>")


class BlockquoteTests(unittest.TestCase):
    def test_simple_and_soft_breaks(self):
        self.assertEqual(render("> a\n> b"), "<blockquote>\n<p>a\nb</p>\n</blockquote>")

    def test_nested_and_lazy(self):
        self.assertEqual(render("> a\n>> b\nlazy"),
                         "<blockquote>\n<p>a</p>\n<blockquote>\n<p>b\nlazy</p>\n</blockquote>\n</blockquote>")

    def test_blockquote_with_list_and_heading(self):
        self.assertEqual(render("> # T\n> - x"),
                         '<blockquote>\n<h2 id="pg--h1">T</h2>\n<ul>\n<li>x</li>\n</ul>\n</blockquote>')


def table(head, body=""):
    return ('<div class="rb-table-wrap"><table class="rb-table">\n<thead>\n<tr>\n' + head
            + "\n</tr>\n</thead>\n<tbody>\n" + body + "</tbody>\n</table></div>")


class TableTests(unittest.TestCase):
    def test_alignment(self):
        out = render("| a | b | c | d |\n|---|:---|:---:|---:|\n| 1 | 2 | 3 | 4 |")
        head = ('<th>a</th>\n<th style="text-align:left">b</th>\n<th style="text-align:center">c</th>\n'
                '<th style="text-align:right">d</th>')
        body = ('<tr>\n<td>1</td>\n<td style="text-align:left">2</td>\n<td style="text-align:center">3</td>\n'
                '<td style="text-align:right">4</td>\n</tr>\n')
        self.assertEqual(out, table(head, body))

    def test_header_only(self):
        self.assertEqual(render("| a | b |\n|---|---|"), table("<th>a</th>\n<th>b</th>"))

    def test_escaped_pipes_inline_and_escaping(self):
        out = render("| x |\n|---|\n| `a\\|b` **c\\|d** <e> |")
        self.assertIn("<td><code>a|b</code> <strong>c|d</strong> &lt;e&gt;</td>", out)

    def test_without_outer_pipes_and_ragged_rows(self):
        out = render("a | b\n--|--\n1\n1 | 2 | 3")
        self.assertIn("<tr>\n<td>1</td>\n<td></td>\n</tr>", out)
        self.assertIn("<tr>\n<td>1</td>\n<td>2</td>\n</tr>", out)
        self.assertNotIn("3", out)

    def test_table_interrupts_paragraph_and_ends_at_blank(self):
        out = render("intro\n| a |\n|---|\n| 1 |\n\nafter")
        self.assertTrue(out.startswith("<p>intro</p>\n<div class=\"rb-table-wrap\">"))
        self.assertTrue(out.endswith("</table></div>\n<p>after</p>"))

    def test_mismatched_delimiter_is_paragraph(self):
        self.assertEqual(render("| a | b |\n|---|"), "<p>| a | b |\n|---|</p>")

    def test_links_in_cells(self):
        out = render("| doc |\n|---|\n| [M](#gf-mission) |")
        self.assertIn('<td><a class="rb-xref" href="#p-gf-mission">M</a></td>', out)


class CodeFenceTests(unittest.TestCase):
    def test_backtick_fence_with_lang(self):
        self.assertEqual(render("```python\nif a < b:\n    print('&')\n```"),
                         '<pre class="rb-code" data-lang="python"><code>if a &lt; b:\n'
                         "    print(&#x27;&amp;&#x27;)</code></pre>")

    def test_tilde_fence_and_default_lang(self):
        self.assertEqual(render("~~~\n**x**\n~~~"), '<pre class="rb-code" data-lang="text"><code>**x**</code></pre>')

    def test_info_string_first_word_and_escape(self):
        self.assertEqual(render('```js "q" title\nx\n```'),
                         '<pre class="rb-code" data-lang="js"><code>x</code></pre>')
        self.assertIn('data-lang="a&lt;b"', render("```a<b\nx\n```"))

    def test_longer_fence_contains_shorter(self):
        out = render("````markdown\n```cmd\n# bash\n```\n````")
        self.assertEqual(out, '<pre class="rb-code" data-lang="markdown"><code>```cmd\n# bash\n```</code></pre>')

    def test_indented_fence_strips_indent(self):
        self.assertEqual(render("  ```\n  a\n    b\n  ```"),
                         '<pre class="rb-code" data-lang="text"><code>a\n  b</code></pre>')

    def test_unclosed_plain_fence_runs_to_end(self):
        self.assertEqual(render("```\na\n\nb"), '<pre class="rb-code" data-lang="text"><code>a\n\nb</code></pre>')

    def test_fence_interrupts_paragraph(self):
        self.assertEqual(render("p\n```\nc\n```"), '<p>p</p>\n<pre class="rb-code" data-lang="text"><code>c</code></pre>')


CMD_TABS = ('<div class="rb-cmd-tabs" role="tablist"><button type="button" class="rb-cmd-tab" '
            'data-shell="powershell">PowerShell</button><button type="button" class="rb-cmd-tab" '
            'data-shell="bash">bash</button></div>')


class CmdTests(unittest.TestCase):
    def test_tabs_exact_markup(self):
        out = render(fence("cmd", "# powershell", "& '.\\x.exe' <a>", "", "# bash", "./x \\", "  --y", ""))
        self.assertEqual(out, '<div class="rb-cmd">' + CMD_TABS
                         + '<pre class="rb-code" data-lang="powershell" data-shell="powershell"><code>'
                           "&amp; &#x27;.\\x.exe&#x27; &lt;a&gt;</code></pre>"
                         + '<pre class="rb-code" data-lang="bash" data-shell="bash"><code>./x \\\n  --y</code></pre>'
                         + "</div>")

    def test_bash_first_still_emits_powershell_first(self):
        out = render(fence("cmd", "# bash", "ls", "# powershell", "dir"))
        self.assertLess(out.index('data-shell="powershell"><code>dir'), out.index('data-shell="bash"><code>ls'))

    def test_no_markers_single_text_pre(self):
        self.assertEqual(render(fence("cmd", "python --version")),
                         '<pre class="rb-code" data-lang="text"><code>python --version</code></pre>')

    def test_errors(self):
        bad = [
            fence("cmd", "echo hi", "# powershell", "a", "# bash", "b"),
            fence("cmd", "# powershell", "a"),
            fence("cmd", "# powershell", "a", "# bash", "b", "# bash", "c"),
            fence("cmd", "# powershell", "", "# bash", "b"),
            fence("cmd extra", "# powershell", "a", "# bash", "b"),
            "```cmd\n# powershell\na\n# bash\nb\n",
        ]
        for md in bad:
            with self.assertRaises(MarkdownError, msg=md):
                render(md)


class CalloutTests(unittest.TestCase):
    def test_every_kind(self):
        for kind in ("info", "tip", "warning", "danger"):
            out = render(fence("callout " + kind, "Title `t`", "Body **b**", "", "- item"))
            self.assertEqual(out, f'<div class="rb-callout rb-callout-{kind}"><div class="rb-callout-title">'
                                  "Title <code>t</code></div><div class=\"rb-callout-body\"><p>Body <strong>b</strong>"
                                  "</p>\n<ul>\n<li>item</li>\n</ul></div></div>")

    def test_title_only_and_escaping(self):
        self.assertEqual(render(fence("callout tip", "", "<T>")),
                         '<div class="rb-callout rb-callout-tip"><div class="rb-callout-title">&lt;T&gt;</div>'
                         '<div class="rb-callout-body"></div></div>')

    def test_body_headings_tasks_and_links_use_page_counters(self):
        rec = Recorder()
        out = render("# A\n" + fence("callout info", "T", "## B", "- [ ] t", "[e](#environment)"), page="x", rec=rec)
        self.assertIn('<h3 id="x--h2">B</h3>', out)
        self.assertIn('data-check="x:1"', out)
        self.assertIn('href="#p-environment"', out)

    def test_errors(self):
        for md in (fence("callout", "T"), fence("callout note", "T"), fence("callout info extra", "T"),
                   fence("callout warning", "", "  "), "```callout info\nT\nbody"):
            with self.assertRaises(MarkdownError, msg=md):
                render(md)


INC = "zip=pkg.zip path=agentic-workshop/x/01-doc.md"


class IncludeTests(unittest.TestCase):
    def test_markup_heading_shift_and_ids(self):
        rec = Recorder(includes={("pkg.zip", "agentic-workshop/x/01-doc.md"): "# Doc\n\n## Sub\n\ntext <b>"})
        out = render("# Page\n\n" + fence("include", INC), page="pg", rec=rec)
        self.assertEqual(out, '<h2 id="pg--h1">Page</h2>\n'
                              '<section class="rb-include" data-source="pkg.zip:agentic-workshop/x/01-doc.md">'
                              '<div class="rb-include-meta">來源文件：<code>01-doc.md</code>'
                              '<script type="application/json" class="rb-include-src">"# Doc\\n\\n## Sub\\n\\ntext <b>"</script></div>\n'
                              '<h2 id="pg--h2">Doc</h2>\n<h3 id="pg--h3">Sub</h3>\n<p>text &lt;b&gt;</p>\n</section>')
        self.assertEqual(rec.include_calls, [("pkg.zip", "agentic-workshop/x/01-doc.md")])

    def test_exportall_block(self):
        self.assertEqual(render(fence("exportall", "")), '<div class="rb-export-all"></div>')
        with self.assertRaises(MarkdownError):
            render(fence("exportall", "x"))

    def test_include_drops_reader_note(self):
        doc = "# Doc\r\n\r\n> 讀者：小組。使用時機：B3。\r\n> 前置條件：無。\r\n\r\nBody\r\n\r\n> 讀者：kept later\r\n"
        out = render(fence("include", INC), page="pg", rec=Recorder(includes={("pkg.zip", "agentic-workshop/x/01-doc.md"): doc}))
        self.assertNotIn("使用時機", out)
        self.assertIn("kept later", out)
        self.assertIn('"# Doc\\r\\n\\r\\nBody', out)

    def test_links_inside_include_get_source_path(self):
        rec = Recorder(includes={("pkg.zip", "a/b.md"): "[c](c.md) [p](#page)"}, links={"c.md": "#p-c"})
        out = render(fence("include", "zip=pkg.zip path=a/b.md") + "\n[d](d.md)", rec=rec, source="chapter")
        self.assertIn('<a class="rb-xref" href="#p-c">c</a> p', out)
        self.assertEqual(rec.link_calls, [("c.md", "a/b.md"), ("#page", "a/b.md"), ("d.md", "chapter")])

    def test_task_numbering_across_includes(self):
        rec = Recorder(includes={("z.zip", "t.md"): "- [ ] inc1\n- [ ] inc2"})
        out = render("- [ ] before\n\n" + fence("include", "zip=z.zip path=t.md") + "\n\n- [ ] after", page="b3", rec=rec)
        self.assertEqual(re.findall(r'data-check="([^"]+)"', out), ["b3:1", "b3:2", "b3:3", "b3:4"])
        self.assertLess(out.index("before"), out.index("inc1"))
        self.assertLess(out.index("inc2"), out.index("after"))

    def test_recursive_include(self):
        rec = Recorder(includes={("z.zip", "a.md"): "# A\n" + fence("include", "zip=z.zip path=sub/b.md"),
                                 ("z.zip", "sub/b.md"): "# B\n[x](x.md)"},
                       links={})
        out = render(fence("include", "zip=z.zip path=a.md"), rec=rec, heading_shift=2)
        self.assertEqual(out.count('<section class="rb-include"'), 2)
        self.assertIn('<h3 id="pg--h1">A</h3>', out)
        self.assertIn('<h3 id="pg--h2">B</h3>', out)
        self.assertIn("<code>b.md</code>", out)
        self.assertEqual(rec.link_calls, [("x.md", "sub/b.md")])

    def test_include_cycle_is_error(self):
        rec = Recorder(includes={("z.zip", "a.md"): fence("include", "zip=z.zip path=b.md"),
                                 ("z.zip", "b.md"): fence("include", "zip=z.zip path=a.md")})
        with self.assertRaises(MarkdownError):
            render(fence("include", "zip=z.zip path=a.md"), rec=rec)

    def test_malformed_include_blocks(self):
        for body in ([], ["zip=z.zip"], ["path=a.md"], ["zip=z.zip path=a.md extra=1"],
                     ["zip=z.zip path=a.md", "zip=z.zip path=b.md"], ["zip= path=a.md"], ["junk"]):
            with self.assertRaises(MarkdownError, msg=body):
                render(fence("include", *body), rec=Recorder(includes={("z.zip", "a.md"): "x"}))
        with self.assertRaises(MarkdownError):
            render(fence("include x", "zip=z.zip path=a.md"), rec=Recorder(includes={("z.zip", "a.md"): "x"}))


class DownloadTests(unittest.TestCase):
    def test_markup_and_callback(self):
        rec = Recorder()
        out = render(fence("download", "id=g0 zip=participant-07-g0.zip label=下載 G0 <Starter> Repository"), rec=rec)
        self.assertEqual(out, '<div class="rb-download-card"><button type="button" class="rb-download" '
                              'data-download="g0" data-filename="g0.zip">下載 G0 &lt;Starter&gt; Repository</button>'
                              '<span class="rb-download-meta">ZIP · 23 KB · SHA256 abcdef012345</span></div>')
        self.assertEqual(rec.download_calls, [("g0", "participant-07-g0.zip", "下載 G0 <Starter> Repository")])

    def test_errors(self):
        for body in (["id=g0 zip=a.zip"], ["zip=a.zip label=x"], ["id=g0 label=x"], ["id=g 0 zip=a.zip label=x"],
                     ["id=../x zip=a.zip label=x"], ["id=g0 zip=a.zip label="]):
            with self.assertRaises(MarkdownError, msg=body):
                render(fence("download", *body))

    def test_bad_register_result(self):
        rec = Recorder()
        rec.register = lambda *a: {"size_kb": "23", "sha12": "x"}
        with self.assertRaises(MarkdownError):
            render(fence("download", "id=g0 zip=a.zip label=x"), rec=rec)


def form_def(html_out):
    m = re.fullmatch(r'<div class="rb-form" data-form-id="([^"]+)"><script type="application/json" '
                     r'class="rb-form-def">(.*)</script></div>', html_out, re.S)
    if not m:
        raise AssertionError("not a form: " + html_out)
    return m.group(1), json.loads(m.group(2))


class FormTests(unittest.TestCase):
    FORM = {"id": "reflection", "title": "回顧 </script> & <x>", "fields": [
        {"id": "a", "label": "A", "type": "textarea", "hint": "h"},
        {"id": "b", "label": "B", "type": "select", "options": ["是", "否"]},
        {"id": "c", "label": "C", "type": "checklist", "items": ["x", "y"]},
        {"id": "d", "label": "D", "type": "checkbox"},
        {"id": "e", "label": "E", "type": "text", "value": "v", "readonly": True}]}

    def test_valid_form_roundtrip_and_script_safety(self):
        out = render(fence("form", json.dumps(self.FORM, ensure_ascii=False, indent=2)))
        form_id, obj = form_def(out)
        self.assertEqual(form_id, "reflection")
        self.assertEqual(obj, self.FORM)
        self.assertNotIn("</script> &", out)
        self.assertEqual(out.count("</script>"), 1)
        self.assertIn("\\u003c/script\\u003e \\u0026 \\u003cx\\u003e", out)

    def test_suggestions_accepted(self):
        sug = ["沒有", {"label": "Rule 範本", "text": "Rule 〈ID〉：〈內容〉"}]
        obj = {"id": "f1", "title": "T", "fields": [{"id": "a", "label": "A", "type": "textarea", "suggestions": sug}]}
        self.assertEqual(form_def(render(fence("form", json.dumps(obj, ensure_ascii=False))))[1], obj)

    def test_validation_errors(self):
        def variant(**changes):
            obj = json.loads(json.dumps(self.FORM))
            obj.update(changes)
            return json.dumps(obj)

        field = {"id": "f", "label": "F", "type": "text"}
        bad = [
            "{not json", "[1, 2]", "", variant(id=None), variant(id=""), variant(id="a b"), variant(title=""),
            variant(fields=[]), variant(fields="x"), variant(extra=1),
            variant(fields=[{**field, "type": "radio"}]), variant(fields=[{"id": "f", "type": "text"}]),
            variant(fields=[{**field, "type": "select"}]), variant(fields=[{**field, "type": "select", "options": []}]),
            variant(fields=[{**field, "type": "checklist"}]), variant(fields=[field, field]),
            variant(fields=[{**field, "placeholder": "p"}]), variant(fields=[{**field, "readonly": "yes"}]),
            variant(fields=["f"]),
            variant(fields=[{**field, "suggestions": []}]), variant(fields=[{**field, "suggestions": [""]}]),
            variant(fields=[{**field, "suggestions": [{"label": "a"}]}]),
            variant(fields=[{**field, "type": "checkbox", "suggestions": ["a"]}]),
        ]
        bad.append(json.dumps({k: v for k, v in self.FORM.items() if k != "title"}))
        bad.append(json.dumps({k: v for k, v in self.FORM.items() if k != "fields"}))
        for body in bad:
            with self.assertRaises(MarkdownError, msg=body):
                render(fence("form", body))


class GateTests(unittest.TestCase):
    EXPECTED = {"id": "gate1", "title": "Gate 核准決策 · GATE1", "kind": "gate", "fields": [
        {"id": "gate_id", "label": "Gate 編號", "type": "text", "value": "GATE1", "readonly": True},
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
         "suggestions": [{"label": "分鐘範本", "text": "第 〈分〉 分鐘"}]}]}

    def test_make_gate_def(self):
        self.assertEqual(make_gate_def("gate1"), self.EXPECTED)
        self.assertEqual(json.dumps(make_gate_def("gate1")), json.dumps(self.EXPECTED))

    def test_gate_block_renders_form(self):
        form_id, obj = form_def(render(fence("gate", "id=gate1")))
        self.assertEqual((form_id, obj), ("gate1", self.EXPECTED))

    def test_errors(self):
        for body in ([], ["gate1"], ["id="], ["id=gate1 x=1"], ["id=<g>"]):
            with self.assertRaises(MarkdownError, msg=body):
                render(fence("gate", *body))
        for bad in ("", "a b", "<x>", None):
            with self.assertRaises(MarkdownError):
                make_gate_def(bad)


@unittest.skipUnless(DIST.is_dir() and CONTENT.is_dir(), "dist candidate or runbook content missing")
class RealChapterSmokeTests(unittest.TestCase):
    """Render every real chapter; includes are read from the candidate zips (never from scratch copies)."""

    def setUp(self):
        self.zips = {}

    def tearDown(self):
        for archive in self.zips.values():
            archive.close()

    def load(self, zip_name, path):
        if zip_name not in self.zips:
            self.zips[zip_name] = zipfile.ZipFile(DIST / zip_name)
        return self.zips[zip_name].read(path).decode("utf-8")

    def test_render_all_chapters(self):
        chapters = sorted(CONTENT.glob("*.md"))
        self.assertTrue(chapters)
        page_ids = set()
        for chapter in chapters:
            meta, body = parse_front_matter(chapter.read_text(encoding="utf-8"))
            for key in ("id", "title", "minute", "group", "section"):
                self.assertIn(key, meta, chapter.name)
            page_ids.add(meta["id"])
        for chapter in chapters:
            with self.subTest(chapter=chapter.name):
                meta, body = parse_front_matter(chapter.read_text(encoding="utf-8"))
                downloads = []

                def resolve(href, source):
                    return "#p-" + href[1:] if href.startswith("#") and href[1:] in page_ids else None

                def register(did, zip_name, label):
                    downloads.append(did)
                    size = (DIST / zip_name).stat().st_size
                    return {"size_kb": max(1, round(size / 1024)), "sha12": "0" * 12}

                ctx = RenderContext(meta["id"], resolve, self.load, register)
                out = render_markdown(body, ctx)
                self.assertEqual(len(downloads), out.count('class="rb-download-card"'))
                again = render_markdown(body, RenderContext(meta["id"], resolve, self.load, register))
                self.assertEqual(out, again)
                ids = re.findall(r'<h[2-6] id="([^"]+)"', out)
                self.assertEqual(ids, [f"{meta['id']}--h{n}" for n in range(1, len(ids) + 1)])
                self.assertEqual(len(ids), ctx.heading_counter)
                self.assertNotIn("<h1", out)
                checks = re.findall(r'data-check="([^"]+)"', out)
                self.assertEqual(checks, [f"{meta['id']}:{n}" for n in range(1, len(checks) + 1)])
                self.assertEqual(len(checks), ctx.task_counter)
                hrefs = re.findall(r'href="([^"]*)"', out)
                self.assertTrue(all(h.startswith("#p-") for h in hrefs), hrefs)
                tags = set(re.findall(r"<([a-z][a-z0-9]*)", out))
                allowed = {"h2", "h3", "h4", "h5", "h6", "p", "strong", "em", "code", "a", "ul", "ol", "li",
                           "label", "input", "span", "blockquote", "hr", "br", "div", "table", "thead", "tbody",
                           "tr", "th", "td", "pre", "button", "section", "script"}
                self.assertLessEqual(tags, allowed)
                self.assertEqual(out.count("<script"), out.count('<script type="application/json" class="rb-form-def">')
                                 + out.count('<script type="application/json" class="rb-include-src">'))
                for _, raw in re.findall(r'data-form-id="([^"]+)"><script[^>]*>(.*?)</script>', out, re.S):
                    self.assertIn("fields", json.loads(raw))


if __name__ == "__main__":
    unittest.main()
