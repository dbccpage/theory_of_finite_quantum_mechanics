"""docs/ is built by GitHub Pages with Jekyll, which runs Liquid over every page before Markdown: a literal `{{` or `{%`
anywhere in a page (code spans included) fails the whole site build. Write them as HTML entities (&#123;&#123;, &#123;%)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIQUID = re.compile(r'\{\{|\{%')


def test_no_liquid_markers_in_published_docs():
    offenders = []
    for path in sorted((ROOT / 'docs').rglob('*.md')):
        text = path.read_text(encoding='utf-8', errors='replace')
        for number, line in enumerate(text.splitlines(), 1):
            if LIQUID.search(line):
                offenders.append('%s:%d' % (path.relative_to(ROOT).as_posix(), number))
    assert not offenders, 'Liquid markers break the Pages build: ' + ', '.join(offenders[:20])
