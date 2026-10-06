"""Build standalone stage decks from local, reviewed speech sources."""
from pathlib import Path
import argparse
import html
import json

ROOT = Path(__file__).resolve().parent


def build_greenfield(check=False):
    stage = ROOT / '01-greenfield'
    slides = json.loads((stage / 'src/slides.json').read_text(encoding='utf-8'))
    ids = set()
    for slide in slides:
        for key in ('id', 'chapter', 'title', 'lead', 'check', 'notes'):
            if not slide.get(key):
                raise ValueError(f'Missing {key}: {slide}')
        if slide['id'] in ids:
            raise ValueError(f'Duplicate id: {slide["id"]}')
        ids.add(slide['id'])
    handout = ['# Greenfield：從 Idea 到可開發的專案',
               '> 讀者：學員。時機：45分鐘引導操作。前置：獨立練習目錄與可用的Coding Agent。',
               '在新目錄進行；每步由人確認。程式與測試未執行時，標記未驗證。']
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
    handout.append('## 完成條件\n至少一條需求到情境與模組的追溯鏈，附已確認決策、缺項與下一步；實測需另有證據。')
    handout_text = '\n\n'.join(handout) + '\n'
    data = {'slides': slides, 'handout': handout_text,
            'idea': (stage / 'practice/idea.md').read_text(encoding='utf-8'),
            'feature': (stage / 'practice/booking.feature').read_text(encoding='utf-8')}
    # Escape HTML-sensitive characters in inline JSON, including closing script tags.
    encoded = json.dumps(data, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    output = (ROOT / 'shared/deck.template.html').read_text(encoding='utf-8')
    replacements = {'TITLE': html.escape('Greenfield：從 Idea 到可開發的專案'),
                    'STYLE': (ROOT / 'shared/deck.css').read_text(encoding='utf-8'),
                    'DATA': 'const SPEECH_DATA = ' + encoded + ';',
                    'SCRIPT': (ROOT / 'shared/deck.js').read_text(encoding='utf-8')}
    for key, value in replacements.items():
        output = output.replace('{{' + key + '}}', value)
    for path, value in [(stage / 'greenfield-deck.html', output),
                        (stage / 'greenfield-handout.md', handout_text)]:
        if check:
            if not path.exists() or path.read_text(encoding='utf-8') != value:
                raise ValueError(f'Outdated build: {path}')
        else:
            path.write_text(value, encoding='utf-8', newline='\n')
    print(f'{"CHECK" if check else "BUILD"} PASS: {len(slides)} slides; standalone HTML and handout')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    build_greenfield(args.check)
