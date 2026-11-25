"""Generate bilingual recall sheets from the expressions in reviewed course material."""
import os
import tempfile
import unicodedata
from pathlib import Path

import omni_core as core
import omni_learning_store as store
from omni_quiz_schema import key_revision, require, text


def normalized(value):
    return ' '.join(unicodedata.normalize('NFKC', value).casefold().split())


def validate_profile(profile):
    fields = {'native', 'target', 'starting_point', 'goal'}
    require(isinstance(profile, dict) and set(profile) == fields and
            all(text(profile[field]) and len(profile[field]) <= 500 for field in fields),
            'A language course needs the native and target language names, starting_point and goal.')
    require(normalized(profile['native']) != normalized(profile['target']),
            'Use distinct native and target languages.')


def validate_plan(config, plan):
    if 'language_course' in config:
        require(all(text(day.get('can_do')) for day in plan['days']),
                'Describe one observable can_do task for each language course day.')


def validate_items(lesson):
    items = lesson.get('language_items')
    require(isinstance(items, list) and bool(items), 'A language lesson needs language_items from its teaching sections.')
    sources = {source['id'] for source in lesson['sources']}
    seen = set()
    for item in items:
        require(isinstance(item, dict) and set(item) == {'form', 'meaning', 'section_index', 'source_id'} and
                all(text(item[k]) for k in ('form', 'meaning', 'source_id')),
                'Provide the taught form, contextual meaning, section_index and source_id.')
        sid, index = item['source_id'], item['section_index']
        require(type(index) is int and 0 <= index < len(lesson['sections']) and sid in sources,
                'Expression needs its taught section and a lesson source.')
        body = lesson['sections'][index]['body']
        require(all(fragment in body for fragment in (item['form'], item['meaning'], f'[{sid}]')),
                'The target form, contextual meaning and citation must occur in the selected teaching section.')
        pair = (normalized(item['form']), normalized(item['meaning']))
        require(pair not in seen, 'Duplicate expression and meaning within the lesson.')
        seen.add(pair)
    return items


def practice(lessons, current, profile, *, answers, reverse=False):
    """Use separate items for the two directions and reverse roles on the next day."""
    from omni_document import material_markdown as escape

    current_lesson = lessons[-1][1]
    lines = [f"# {escape(current_lesson['title'])} · Day{current:02d}", '']
    used_forms, used_meanings = set(), set()
    # Give current learning priority when the learner selected overlapping review days.
    for day, lesson in reversed(lessons):
        for index, item in enumerate(validate_items(lesson)):
            form, meaning = item['form'], item['meaning']
            if normalized(form) in used_forms or normalized(meaning) in used_meanings:
                continue
            used_forms.add(normalized(form))
            used_meanings.add(normalized(meaning))
            if (index + current - day + int(reverse)) % 2 == 0:
                direction = f"{profile['target']} → {profile['native']}"
                question, response = form, meaning
            else:
                direction = f"{profile['native']} → {profile['target']}"
                question, response = meaning, form
            number = len(used_forms)
            lines.extend([f"**{number}. {escape(direction)}**", '', escape(question), ''])
            if answers:
                lines.extend([f"→ {escape(response)}  ·  Day{day:02d} [{item['source_id']}]", ''])
            else:
                lines.extend(['＿＿＿＿＿＿＿＿＿＿＿＿', ''])
    return '\n'.join(lines)


def worksheet(root, key, review_from, *, answers, reverse=False):
    from omni_quiz import snapshot

    root = Path(root).resolve()
    profile = core.read(root / 'config.json').get('language_course')
    validate_profile(profile)
    key_revision(key, 1)
    day = int(key[3:])
    require(key == f'Day{day:02d}', 'Use the canonical DayNN lesson key.')
    lesson, _, state = snapshot(root, key)
    review = []
    for previous in review_from:
        key_revision(previous, 1)
        number = int(previous[3:])
        require(previous == f'Day{number:02d}' and number < day and str(number) in state['lessons'],
                'Review requires an earlier delivered lesson from this same course.')
        if number not in review:
            review.append(number)
    review.sort()
    past = [(n, snapshot(root, f'Day{n:02d}')[0]) for n in review]
    return practice([*past, (day, lesson)], day, profile, answers=answers, reverse=reverse)


def configure(commands):
    actions = commands.add_parser('language').add_subparsers(dest='language_action', required=True)
    for action in ('worksheet', 'answer-key'):
        parser = actions.add_parser(action)
        parser.add_argument('--key', required=True)
        parser.add_argument('--review-from', action='append', default=[])
        parser.add_argument('--reverse', action='store_true', help='Swap the recall direction for every expression.')


def execute(root, args):
    root = Path(root).resolve()
    answers = args.language_action == 'answer-key'
    with core.lock(root):
        content = worksheet(root, args.key, args.review_from, answers=answers, reverse=args.reverse)
        # Immutable content names make retries idempotent and keep old sheets usable.
        name = f'{args.key}-{args.language_action}-{store.fingerprint(content)[:12]}.md'
        path = store.path(root, 'language-keys' if answers else 'language-worksheets', name)
        path.parent.parent.mkdir(mode=0o700, exist_ok=True)
        path.parent.mkdir(mode=0o700, exist_ok=True)
        if path.exists():
            require(path.read_text(encoding='utf-8') == content, 'Previously generated worksheet was edited.')
        else:
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(dir=path.parent, delete=False, mode='w', encoding='utf-8') as stream:
                    temporary = Path(stream.name)
                    stream.write(content)
                os.replace(temporary, path)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
    return {'path': str(path.relative_to(root)), 'kind': args.language_action}
