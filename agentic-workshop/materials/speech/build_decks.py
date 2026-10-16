"""Build standalone stage decks from local, reviewed speech sources.

Every stage folder with src/stage.json and src/slides.json, here and in materials-dlc/speech/,
is built into <deck> and <handout> with the shared/ template.
"""
from pathlib import Path
import argparse
import html
import json

ROOT = Path(__file__).resolve().parent
STAGE_ROOTS = (ROOT, ROOT.parents[1] / 'materials-dlc/speech')
SLIDE_KEYS = ('id', 'chapter', 'title', 'lead', 'check', 'notes')
STAGE_KEYS = ('title', 'header', 'minutes', 'deck', 'handout', 'handout_intro', 'handout_done')


def stages():
    return sorted(p.parent.parent for r in STAGE_ROOTS for p in r.glob('*/src/stage.json'))


def build_stage(stage, check=False):
    meta = json.loads((stage / 'src/stage.json').read_text(encoding='utf-8'))
    for key in STAGE_KEYS:
        if not meta.get(key):
            raise ValueError(f'{stage.name}: missing stage {key}')
    slides = json.loads((stage / 'src/slides.json').read_text(encoding='utf-8'))
    ids = set()
    for slide in slides:
        for key in SLIDE_KEYS:
            if not slide.get(key):
                raise ValueError(f'{stage.name}: missing {key}: {slide}')
        if slide['id'] in ids:
            raise ValueError(f'{stage.name}: duplicate id: {slide["id"]}')
        ids.add(slide['id'])
    handout = ['# ' + meta['title'], *meta['handout_intro']]
    for number, slide in enumerate(slides, 1):
        handout.extend([f'## {number}. {slide["title"]}', slide['lead']])
        if slide.get('flow'):
            handout.append(' → '.join(slide['flow']))
        for title, body in slide.get('cards', []):
            handout.append(f'- **{title}**：{body}')
        if slide.get('code'):
            handout.append('```text\n' + slide['code'] + '\n```')
        if slide.get('prompt'):
            handout.extend(['### 交給 Agent 的指令', slide['prompt']])
        handout.append('**人工確認**：' + slide['check'])
    handout.append('## 完成條件\n' + meta['handout_done'])
    handout_text = '\n\n'.join(handout) + '\n'
    downloads = [{'label': d['label'], 'name': d['name'],
                  'text': (stage / d['file']).read_text(encoding='utf-8')} for d in meta.get('downloads', [])]
    downloads.append({'label': '下載操作講義', 'name': meta['handout'], 'text': handout_text})
    data = {'slides': slides, 'title': meta['title'], 'minutes': meta['minutes'], 'downloads': downloads}
    # Escape HTML-sensitive characters in inline JSON, including closing script tags.
    encoded = json.dumps(data, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    output = (ROOT / 'shared/deck.template.html').read_text(encoding='utf-8')
    replacements = {'TITLE': html.escape(meta['title']),
                    'HEADER': html.escape(meta['header']),
                    'MINUTES': f'{meta["minutes"]:02d}',
                    'STYLE': (ROOT / 'shared/deck.css').read_text(encoding='utf-8'),
                    'DATA': 'const SPEECH_DATA = ' + encoded + ';',
                    'SCRIPT': (ROOT / 'shared/deck.js').read_text(encoding='utf-8')}
    for key, value in replacements.items():
        output = output.replace('{{' + key + '}}', value)
    for path, value in [(stage / meta['deck'], output), (stage / meta['handout'], handout_text)]:
        if check:
            if not path.exists() or path.read_text(encoding='utf-8') != value:
                raise ValueError(f'Outdated build: {path}')
        else:
            path.write_text(value, encoding='utf-8', newline='\n')
    print(f'{"CHECK" if check else "BUILD"} PASS: {stage.name}: {len(slides)} slides; standalone HTML and handout')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('only', nargs='*', help='stage folder names (default: all)')
    args = parser.parse_args()
    for stage in stages():
        if args.only and stage.name not in args.only:
            continue
        build_stage(stage, args.check)
