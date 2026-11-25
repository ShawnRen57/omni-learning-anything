"""Readable, source-linked lesson figures. Pillow is needed only to draw a new PNG."""
import hashlib
import io
import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
from pathlib import Path


def _text(value, name, limit):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f'Provide a nonempty {name} of at most {limit} characters.')
    return value.strip()


def validate_reading(figure, source_ids, *, required):
    reading = figure.get('reading')
    if reading is None and not required:
        return
    if not isinstance(reading, dict):
        raise ValueError('Add figure.reading with a question, a visible observation and source_ids.')
    question = _text(reading.get('question'), 'figure question', 260)
    observation = _text(reading.get('observation'), 'figure observation', 450)
    if question == observation:
        raise ValueError('Describe the visual evidence that answers the question.')
    refs = reading.get('source_ids')
    if (not isinstance(refs, list) or not refs
            or any(not isinstance(ref, str) or not re.fullmatch(r'S\d+', ref) for ref in refs)
            or len(set(refs)) != len(refs) or not set(refs).issubset(source_ids)):
        raise ValueError('Figure source_ids must point to distinct sources in this document.')


def caption(figure):
    reading = figure.get('reading')
    if not reading:
        return figure['caption']
    refs = ' '.join(f'[{ref}]' for ref in reading['source_ids'])
    return ' '.join((figure['caption'], reading['question'], reading['observation'], refs))


def _strings(items, name, minimum, maximum, text_limit):
    if not isinstance(items, list) or not minimum <= len(items) <= maximum:
        raise ValueError(f'Provide {minimum}–{maximum} {name} entries.')
    return [_text(item, name, text_limit) for item in items]


def _table(spec):
    """Return a grid of cells in reading order; the border/arrow conveys the layout."""
    if spec.get('layout') == 'sequence':
        steps = spec.get('steps')
        if not isinstance(steps, list) or not 2 <= len(steps) <= 4 or not all(isinstance(s, dict) for s in steps):
            raise ValueError('A sequence needs two to four steps with label and detail.')
        return [[_text(s.get('label'), 'step label', 55) for s in steps],
                [_text(s.get('detail'), 'step detail', 130) for s in steps]]
    if spec.get('layout') != 'comparison':
        raise ValueError('Choose comparison, sequence or fraction-bars for the figure layout.')
    columns = _strings(spec.get('columns'), 'column', 2, 3, 55)
    if len(set(columns)) != len(columns):
        raise ValueError('Comparison columns must identify different subjects.')
    rows = spec.get('rows')
    if not isinstance(rows, list) or not 1 <= len(rows) <= 4 or not all(isinstance(r, dict) for r in rows):
        raise ValueError('A comparison needs one to four labeled rows.')
    return [['', *columns]] + [[_text(row.get('label'), 'row label', 55),
                                *_strings(row.get('values'), 'comparison value', len(columns), len(columns), 110)]
                               for row in rows]


def _font_candidates(chars):
    # Prefer fonts for the actual scripts. Pillow's FreeType renderer does not
    # implicitly fall back to another family when a code point is unavailable.
    cjk = any('\u3000' <= ch <= '\ud7af' for ch in chars)
    family = 'Noto Sans CJK SC' if cjk else 'DejaVu Sans'
    fontconfig = shutil.which('fc-match')
    if fontconfig:
        query = family + ':charset=' + ' '.join(f'{ord(ch):x}' for ch in sorted(chars))
        try:
            result = subprocess.run([fontconfig, '-s', '-f', '%{file}\n', query],
                                    capture_output=True, text=True, timeout=5)
            yield from result.stdout.splitlines()
        except (OSError, subprocess.TimeoutExpired):
            pass
    for filename in ('/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
                     '/System/Library/Fonts/Supplemental/Arial.ttf',
                     str(Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts/msyh.ttc'),
                     str(Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts/arial.ttf'),
                     '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVuSans.ttf'):
        yield filename


def _font(text, explicit):
    from PIL import ImageFont, features
    chars = {char for char in text if not char.isspace() and unicodedata.category(char) != 'Cf'}
    needs_shaping = any(unicodedata.bidirectional(ch) in ('R', 'AL')
                        or 0x0900 <= ord(ch) <= 0x109F or 0x1780 <= ord(ch) <= 0x17FF for ch in chars)
    if needs_shaping and not features.check('raqm'):
        raise ValueError('These labels require script shaping. Use Pillow with libraqm or a verified diagram from another renderer.')
    candidates = [explicit] if explicit else _font_candidates(chars)
    for path in dict.fromkeys(candidates):
        try:
            probe = ImageFont.truetype(str(path), 32)
            missing = bytes(probe.getmask('\U0010ffff'))
            if all(bytes(probe.getmask(ch)) != missing for ch in chars):
                return probe
        except OSError:
            continue
    raise ValueError('No font covers the diagram labels. Supply --font with an installed Unicode font for both scripts.')


def _lines(text, font, width):
    """Wrap words and unspaced CJK labels, retaining readable minimum type."""
    result = []
    for paragraph in text.splitlines():
        line = ''
        for token in re.findall(r'[\u2e80-\u9fff\uac00-\ud7a3]|[^\s\u2e80-\u9fff\uac00-\ud7a3]+|\s+', paragraph):
            if font.getlength(token) > width:
                raise ValueError('Use a shorter unbroken label so it fits at reading size.')
            if line.strip() and font.getlength(line + token) > width:
                result.append(line.rstrip())
                line = ''
            line += token if line else token.lstrip()
        if line.strip():
            result.append(line.rstrip())
    if len(result) > 5:
        raise ValueError('Shorten the diagram or split its information across lessons.')
    return result


def _draw(spec, grid, font_path):
    from PIL import Image, ImageDraw
    title = spec['title']
    base = _font(''.join([title, *(cell for row in grid for cell in row)]), font_path)
    title_font, heading, body = [base.font_variant(size=size) for size in (47, 36, 34)]
    navy, teal, mut = '#183537', '#196a67', '#d1dedc'
    width, margin = 1440, 48
    flow = spec['layout'] == 'sequence'
    gap = 44 if flow else 4
    count = len(grid[0])
    box_width = (width - 2 * margin - (count - 1) * gap) // count
    titles = _lines(title, title_font, width - 2 * margin)
    grid_top = 42 + len(titles) * 61 + 24
    wrapped, heights = [], []
    for i, row in enumerate(grid):
        cells = [_lines(cell, heading if i == 0 else body, box_width - 48) for cell in row]
        wrapped.append(cells)
        heights.append(48 + 50 * max(len(lines) for lines in cells))
    total = grid_top + sum(heights) + margin
    if total > 1070:
        raise ValueError('Shorten the diagram rows so labels stay readable in the exported lesson.')
    image = Image.new('RGB', (width, total), 'white')
    draw = ImageDraw.Draw(image)
    for i, line in enumerate(titles):
        draw.text((margin, 30 + i * 61), line, font=title_font, fill=navy)
    y = grid_top
    for r, cells in enumerate(wrapped):
        for col, lines in enumerate(cells):
            x = margin + col * (box_width + gap)
            bg = teal if r == 0 else '#eaf2ef' if flow or col == 0 else '#f7f9f8'
            draw.rectangle((x, y, x + box_width, y + heights[r] - 2), fill=bg)
            for i, line in enumerate(lines):
                font = heading if r == 0 else body
                draw.text((x + 24, y + 15 + i * 50), line, font=font, fill='white' if r == 0 else navy)
            if flow and r == 0 and col + 1 < count:
                cx, cy = x + box_width + 5, y + heights[r] // 2
                draw.line((cx, cy, cx + 28, cy), fill=teal, width=4)
                draw.polygon([(cx + 28, cy), (cx + 18, cy - 8), (cx + 18, cy + 8)], fill=teal)
        y += heights[r]
    draw.line((margin, y + 8, width - margin, y + 8), fill=mut, width=2)
    return image


def _fraction_bars(spec, font_path):
    from PIL import Image, ImageDraw
    unit = _text(spec.get('unit'), 'whole unit', 110)
    bars = spec.get('bars')
    if not isinstance(bars, list) or not 2 <= len(bars) <= 4:
        raise ValueError('Provide two to four fraction bars.')
    fractions = []
    for bar in bars:
        if not isinstance(bar, dict):
            raise ValueError('Each fraction needs an integer numerator and denominator.')
        n, d = bar.get('numerator'), bar.get('denominator')
        if type(n) is not int or type(d) is not int or not 0 <= n <= d or not 1 <= d <= 16:
            raise ValueError('A fraction needs 0 <= numerator <= denominator, with denominator from 1 to 16.')
        fractions.append((n, d))

    base = _font(spec['title'] + unit + '0123456789/', font_path)
    title_font = base.font_variant(size=47)
    title_lines = _lines(spec['title'], title_font, 1312)
    unit_lines = _lines(unit, base, 1312)
    unit_y = 34 + len(title_lines) * 62
    axis_y = unit_y + 48 * len(unit_lines) + 75
    left, right, row_gap, bar_height = 210, 1330, 94, 54
    middle = (left + right) // 2
    height = axis_y + 36 + (len(fractions) - 1) * row_gap + bar_height + 52
    image = Image.new('RGB', (1440, height), 'white')
    draw = ImageDraw.Draw(image)
    ink, filled, paper = '#183537', '#196a67', '#eaf2ef'
    for i, line in enumerate(title_lines):
        draw.text((56, 30 + 62 * i), line, font=title_font, fill=ink)
    for i, line in enumerate(unit_lines):
        draw.text((56, unit_y + 48 * i), line, font=base, fill=ink)
    draw.line((left, axis_y, right, axis_y), fill=ink, width=3)
    for x, label in ((left, '0'), (middle, '1/2'), (right, '1')):
        draw.text((x, axis_y - 13), label, anchor='mb', font=base, fill=ink)
        draw.line((x, axis_y - 5, x, axis_y + 7), fill=ink, width=3)
        for dash_y in range(axis_y + 11, height - 52, 13):
            draw.line((x, dash_y, x, dash_y + 6), fill='#617a77', width=2)
    for row, (n, d) in enumerate(fractions):
        y = axis_y + 36 + row * row_gap
        ticks = [left + round((right - left) * i / d) for i in range(d + 1)]
        draw.text((left - 38, y + bar_height // 2), f'{n}/{d}', anchor='rm', font=base, fill=ink)
        draw.rectangle((left, y, right, y + bar_height), fill=paper)
        if n:
            draw.rectangle((left, y, ticks[n], y + bar_height), fill=filled)
        for i, x in enumerate(ticks[1:-1], start=1):
            draw.line((x, y + 2, x, y + bar_height - 2), fill='white' if i < n else ink, width=3)
        draw.rectangle((left, y, right, y + bar_height), outline=ink, width=3)
    return image


def build(root, spec, *, font=None):
    if not isinstance(spec, dict):
        raise ValueError('A diagram specification must be an object.')
    title = _text(spec.get('title'), 'figure title', 140)
    credit = _text(spec.get('credit'), 'figure credit', 300)
    reading = spec.get('reading')
    refs = reading.get('source_ids') if isinstance(reading, dict) else None
    # References can be checked for membership only when the host assembles the document.
    validate_reading(spec, refs if isinstance(refs, list) else [], required=True)
    image = (_fraction_bars(spec, font) if spec.get('layout') == 'fraction-bars'
             else _draw(spec, _table(spec), font))
    output = io.BytesIO()
    image.save(output, format='PNG')
    png = output.getvalue()
    filename = 'diagram-' + hashlib.sha256(png).hexdigest() + '.png'
    root = Path(root).resolve()
    directory = root / 'assets'
    if directory.is_symlink():
        raise ValueError('Keep the diagram assets directory inside the project.')
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    if path.is_symlink():
        raise ValueError('A diagram output must be a regular project asset.')
    temp = tempfile.NamedTemporaryFile(dir=directory, delete=False)
    stage = Path(temp.name)
    try:
        with temp:
            temp.write(png)
        os.replace(stage, path)
    finally:
        stage.unlink(missing_ok=True)
    return {'path': 'assets/' + filename, 'caption': title, 'credit': credit, 'reading': reading}
