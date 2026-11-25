"""Curated source discovery and adaptation to the existing, versioned course binding."""
import unicodedata

KINDS = {
    'course': '公开课', 'textbook': '教材', 'academic_book': '学术书籍',
    'article': '深度文章', 'lecture_series': '系列讲座', 'talk': '单场演讲',
}
ACCESS = {
    'course_material': 'Public syllabus and session materials. Open the chosen session before teaching.',
    'outline': 'Public course information. Enrollment, dates or sign-in may affect access to sessions.',
    'read': 'Public reading entry. Open the selected chapters or sections and verify access.',
    'watch': 'Public talk or lecture entry. Check playback, transcript and language for the chosen segment.',
    'publisher': 'Publisher record only. Detailed study requires readable chapters from an authorized copy.',
}


def _term(value):
    return unicodedata.normalize('NFKC', value).casefold()


def discover(catalog, kind=None, query=None, language=None):
    records = catalog.get('resources', [])
    if kind:
        records = [r for r in records if r['kind'] == kind]
    if language:
        records = [r for r in records if r['language'] == language]
    words = _term(query or '').split()
    results = []
    for r in records:
        values = (r['id'], r['title'], r['zh_title'], r['provider'], r.get('author', ''),
                  r['kind'].replace('_', ' '), KINDS[r['kind']], r['focus'])
        searchable = _term(' '.join(values))
        if all(word in searchable for word in words):
            results.append({k: r[k] for k in ('id', 'kind', 'title', 'zh_title', 'provider', 'language',
                                               'access', 'focus', 'url')})
    return {'checked_at': catalog.get('resources_checked_at'), 'total': len(results), 'resources': results}


def snapshot(resource, checked_at):
    """Use the audited source locators as selectable units in a normal course plan."""
    r = resource
    units = [{'id': f'u{i:02d}', 'title': locator, 'locator': locator, 'source_id': 'O1', 'focus': r['focus']}
             for i, locator in enumerate(r['locators'], 1)]
    source = {'id': 'O1', 'title': r['title'], 'url': r['url'], 'locator': ' / '.join(r['locators']),
              'checked_at': checked_at, 'kind': 'official'}
    return {
        'id': r['id'], 'title': r['title'], 'institution': r['provider'], 'code': r['kind'],
        'edition': r.get('edition', r['title']), 'provider_type': 'source_provider',
        'pathway_type': 'resource', 'resource_kind': r['kind'], 'access_mode': r['access'],
        'original_language': r['language'], 'source_access': ACCESS[r['access']],
        'instructors': [r['author']] if r.get('author') else [],
        'aliases': list(dict.fromkeys([r['zh_title'], r['provider'] + ' ' + r['title']])),
        'domain': r['focus'], 'level': 'Determine from the selected source and learner baseline',
        'prerequisites': [], 'audience': 'Learners choosing this source and an agreed scope',
        'pace': {'description': 'Agree on the relevant chapters, sessions, sections or timestamps.'},
        'evidence_level': 'syllabus_only' if r['access'] in ('outline', 'publisher') else 'syllabus_and_sessions',
        'sources': [source], 'units': units,
    }
