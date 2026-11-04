"""Pinned acquisition, verified local copies and original PDF locators."""
import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills/omni-learning-anything/scripts'))
import omni_materials as materials
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject


def fixture_pdf(*, blank=False, padding=0):
    writer = PdfWriter()
    page = writer.add_blank_page(300, 300)
    if not blank:
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                 NameObject('/Subtype'): NameObject('/Type1'),
                                 NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
        stream = DecodedStreamObject()
        stream.set_data(b'BT /F1 12 Tf 20 200 Td (Textbook evidence.) Tj ET')
        page[NameObject('/Contents')] = stream
    if padding:
        writer.add_attachment('padding.bin', b'x' * padding)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


def source(path, payload, part=None):
    return {'path': path, 'part': part, 'size': len(payload),
            'sha': hashlib.sha1(f'blob {len(payload)}\0'.encode() + payload).hexdigest()}


class TextbookFetchTests(unittest.TestCase):
    def setUp(self):
        import omni_textbook_fetch as fetch
        self.fetch = fetch
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'course'
        self.pdf = fixture_pdf()
        self.book = {'book_id': 'ct-example', 'title': '教材一册',
                     'repository': 'TapXWorld/ChinaTextbook', 'commit': '1' * 40,
                     'sources': [source('目录/教材 一册.pdf', self.pdf)]}

    def test_download_and_reuse_verified_original_with_material_pages(self):
        class Response(io.BytesIO):
            status = 200
            headers = {'Content-Type': 'application/octet-stream', 'Content-Length': str(len(self.pdf))}

        with patch.object(self.fetch.OPENER, 'open', return_value=Response(self.pdf)) as open_url:
            result = self.fetch.acquire(self.root, self.book)
            request = open_url.call_args.args[0]
            self.assertEqual(request.full_url, 'https://raw.githubusercontent.com/TapXWorld/ChinaTextbook/'
                             + self.book['commit'] + '/%E7%9B%AE%E5%BD%95/%E6%95%99%E6%9D%90%20%E4%B8%80%E5%86%8C.pdf')
        with patch.object(self.fetch.OPENER, 'open', side_effect=AssertionError('Unnecessary fetch')):
            cached = self.fetch.acquire(self.root, self.book)
        self.assertEqual(result, cached)
        self.assertEqual(result['sha256'], hashlib.sha256(self.pdf).hexdigest())
        self.assertEqual(self.fetch.source_pdf(self.root, result['book_id'], result['sha256']).read_bytes(), self.pdf)
        self.assertEqual(result['material']['version'], result['sha256'])
        selected = materials.select(self.root, result['material']['id'], result['sha256'], pages='1')
        self.assertIn('PDF page 1', materials.search(self.root, 'evidence', selection=selected)[0]['locator'])

    def test_wrong_segment_bytes_leave_no_original_or_material(self):
        a, b = self.pdf[:50], self.pdf[50:]
        self.book['sources'] = [source('book.pdf.1', a, 1), source('book.pdf.2', b, 2)]
        responses = [io.BytesIO(a), io.BytesIO(b[:-1] + b'x')]
        for response in responses:
            response.status = 200
            response.headers = {'Content-Type': 'application/octet-stream'}
        with patch.object(self.fetch.OPENER, 'open', side_effect=responses) as open_url:
            with self.assertRaisesRegex(ValueError, 'checksum'):
                self.fetch.acquire(self.root, self.book)
            self.assertEqual([call.args[0].full_url.rsplit('/', 1)[-1] for call in open_url.call_args_list],
                             ['book.pdf.1', 'book.pdf.2'])
        self.assertEqual(list(self.root.rglob('*.pdf')), [])
        self.assertEqual(list(self.root.rglob('*.json')), [])

    def test_split_local_copy_checks_each_segment(self):
        self.book['sources'] = [source('book.pdf.1', self.pdf[:40], 1),
                                source('book.pdf.2', self.pdf[40:], 2)]
        path = self.root.parent / 'mine.pdf'
        path.write_bytes(self.pdf)
        with patch.object(self.fetch.OPENER, 'open', side_effect=AssertionError('Unexpected network')):
            result = self.fetch.acquire(self.root, self.book, local_pdf=path)
        self.assertEqual(result['origin'], 'pinned_repository')
        self.assertEqual(result['material']['status'], 'ready')

    def test_private_edition_needs_confirmation_and_does_not_inherit_repository_url(self):
        path = self.root.parent / 'private.pdf'
        path.write_bytes(fixture_pdf(blank=True))
        with self.assertRaisesRegex(ValueError, 'edition'):
            self.fetch.acquire(self.root, self.book, local_pdf=path)
        result = self.fetch.acquire(self.root, self.book, local_pdf=path, confirm_local_edition=True)
        self.assertEqual(result['origin'], 'user_confirmed_edition')
        self.assertIsNone(result['origin_url'])
        snapshot = materials.load(self.root, result['material']['id'], result['sha256'])
        self.assertEqual(snapshot['status'], 'failed')
        self.assertNotIn('url', snapshot)
        self.assertTrue(self.fetch.source_pdf(self.root, result['book_id'], result['sha256']).is_file())

    def test_large_book_import_preserves_pages_and_ordinary_import_limit(self):
        import omni_material_readers as readers
        path = self.root.parent / 'large.pdf'
        path.write_bytes(fixture_pdf(padding=51 * 1024 * 1024))
        self.assertGreater(path.stat().st_size, readers.MAX_FILE)
        result = self.fetch.acquire(self.root, self.book, local_pdf=path, confirm_local_edition=True)
        snapshot = materials.load(self.root, result['material']['id'], result['sha256'])
        self.assertEqual(snapshot['units'][0]['page'], 1)
        with self.assertRaisesRegex(ValueError, '50 MiB'):
            materials.import_file(self.root, path)

    def test_invalid_pdf_and_symlink_are_rejected(self):
        path = self.root.parent / 'invalid.pdf'
        path.write_bytes(b'<html>404</html>')
        with self.assertRaisesRegex(ValueError, 'PDF'):
            self.fetch.acquire(self.root, self.book, local_pdf=path, confirm_local_edition=True)
        link = self.root.parent / 'link.pdf'
        link.symlink_to(path)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.fetch.acquire(self.root, self.book, local_pdf=link, confirm_local_edition=True)
        self.assertEqual(list(self.root.rglob('*.pdf')), [])

    def test_host_redirect_and_unexpected_status_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'redirect'):
            self.fetch.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://example.com/evil')
        response = io.BytesIO(self.pdf)
        response.status = 200
        response.headers = {'Content-Type': 'text/html'}
        with patch.object(self.fetch.OPENER, 'open', return_value=response):
            with self.assertRaisesRegex(ValueError, 'HTML'):
                self.fetch.acquire(self.root, self.book)

    def test_untrusted_index_metadata_is_rejected_before_network(self):
        with patch.object(self.fetch.OPENER, 'open', side_effect=AssertionError('Unexpected network')):
            for sources in ([source('../bad.pdf', self.pdf)], [source('book.pdf.2', self.pdf, 2)],
                            [dict(self.book['sources'][0], size=self.fetch.MAX_TEXTBOOK_BYTES + 1)]):
                with self.subTest(sources=sources):
                    with self.assertRaises(ValueError):
                        self.fetch.acquire(self.root, dict(self.book, sources=sources))
