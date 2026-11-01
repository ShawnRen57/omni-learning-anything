"""Installer boundaries, actual bundle structure and learner-data preservation."""
import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from unittest.mock import patch
from test_documents import SCRIPTS

SKILL=SCRIPTS.parent


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.archive=self.root/'skill.zip'
        self.make_zip(self.archive)
        self.dest=self.root/'skills/omni-learning-anything'

    def tearDown(self):self.tmp.cleanup()

    def engine(self):
        import omni_installation
        return omni_installation

    def make_zip(self,path,mutate=None):
        files={str(p.relative_to(SKILL)):p.read_bytes() for p in SKILL.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        if mutate:mutate(files)
        with ZipFile(path,'w',ZIP_DEFLATED) as z:
            for name,data in files.items():z.writestr('omni-learning-anything/'+name,data)
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def install(self):
        return self.engine().install(self.archive,self.dest,hashlib.sha256(self.archive.read_bytes()).hexdigest())

    def test_fresh_install_receipt_and_discovery_unknown_without_native_inventory(self):
        s=self.engine();result=self.install();self.assertEqual(result['action'],'installed')
        status=s.inspect(self.dest)
        self.assertTrue(status['complete']);self.assertTrue(status['integrity_verified'])
        self.assertEqual(status['native_discovery'],'unknown')
        self.assertFalse(any(self.dest.rglob('config.json')))
        self.assertTrue((self.dest/'.omni-install.json').exists())

    def test_missing_local_import_is_incomplete(self):
        self.install();(self.dest/'scripts/omni_quiz.py').unlink()
        result=self.engine().inspect(self.dest)
        self.assertFalse(result['complete']);self.assertFalse(result['integrity_verified'])

    def test_checksum_and_unsafe_zip_fail_without_target(self):
        s=self.engine()
        with self.assertRaises(ValueError):s.install(self.archive,self.dest,'0'*64)
        for bad in ('../escape','scripts/credentials.json','course/state.json'):
            sha=self.make_zip(self.archive,lambda files:files.update({bad:b'private'}))
            with self.assertRaises(ValueError):s.install(self.archive,self.dest,sha)
            self.assertFalse(self.dest.exists())

    def test_fresh_install_will_not_overwrite_existing(self):
        self.dest.mkdir(parents=True);(self.dest/'notes.txt').write_text('mine')
        with self.assertRaises(ValueError):self.install()
        self.assertEqual((self.dest/'notes.txt').read_text(),'mine')

    def test_managed_upgrade_preserves_outside_data_and_exact_backup(self):
        self.install();s=self.engine();before={str(p.relative_to(self.dest)):p.read_bytes() for p in self.dest.rglob('*') if p.is_file()}
        course=self.root/'courses/topic';course.mkdir(parents=True)
        for name in ('config.json','plan.json','state.json','learning/records.json','receipts/Day01.json'):
            p=course/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('private '+name)
        connections=self.root/'connections';connections.mkdir();(connections/'personal.json').write_text('private profile')
        data={p:p.read_bytes() for p in self.root.rglob('*.json') if not p.is_relative_to(self.dest)}
        updated=self.root/'new.zip';sha=self.make_zip(updated,lambda files:files.update({'references/setup.md':files['references/setup.md']+b'\nUpdated guide.\n'}))
        result=s.install(updated,self.dest,sha,update=True)
        backup=Path(result['backup']);self.assertNotEqual(backup,self.dest)
        for name,content in before.items():self.assertEqual((backup/name).read_bytes(),content)
        for path,content in data.items():self.assertEqual(path.read_bytes(),content)
        self.assertTrue(s.inspect(self.dest)['integrity_verified'])
        self.assertEqual(s.install(updated,self.dest,sha,update=True)['action'],'unchanged')

    def test_edited_unmanaged_or_unknown_files_never_removed(self):
        self.install();s=self.engine();updated=self.root/'new.zip';sha=self.make_zip(updated)
        edited=self.dest/'references/setup.md';edited.write_text('my local edits')
        with self.assertRaises(ValueError):s.install(updated,self.dest,sha,update=True)
        self.assertEqual(edited.read_text(),'my local edits')
        # A native-manager install has no receipt: its own updater must be used.
        (self.dest/'.omni-install.json').unlink()
        with self.assertRaises(ValueError):s.install(updated,self.dest,sha,update=True)

    def test_symlinks_and_zip_duplicates_rejected(self):
        self.install();s=self.engine();outside=self.root/'outside';outside.write_text('private')
        (self.dest/'notes').symlink_to(outside)
        with self.assertRaises(ValueError):s.install(self.archive,self.dest,hashlib.sha256(self.archive.read_bytes()).hexdigest(),update=True)
        self.assertEqual(outside.read_text(),'private')
        with ZipFile(self.archive,'a') as z:z.writestr('omni-learning-anything/SKILL.md',b'other')
        with self.assertRaises(ValueError):s.install(self.archive,self.root/'new',hashlib.sha256(self.archive.read_bytes()).hexdigest())

    def test_failed_swap_restores_old_install(self):
        self.install();s=self.engine();before=(self.dest/'SKILL.md').read_bytes()
        updated=self.root/'new.zip';sha=self.make_zip(updated,lambda files:files.update({'references/setup.md':b'updated'}))
        original=s.os.replace
        def replace(a,b):
            if Path(a).name=='bundle' and Path(b)==self.dest.resolve():raise OSError('simulated rename failure')
            return original(a,b)
        with patch.object(s.os,'replace',side_effect=replace):
            with self.assertRaises(OSError):s.install(updated,self.dest,sha,update=True)
        self.assertEqual((self.dest/'SKILL.md').read_bytes(),before)
        self.assertTrue(s.inspect(self.dest)['integrity_verified'])

    def test_course_archives_cannot_be_initialized_inside_installed_skill(self):
        self.install();import omni_core as c
        for root in (self.dest,self.dest/'courses/topic'):
            with self.assertRaises(ValueError):c.initialize(root,{'timezone':'Asia/Shanghai'},{'topic':'x','days':[{'day':1,'topic':'x'}]})
            self.assertFalse((root/'state.json').exists())

    def test_missing_linked_reference_is_incomplete(self):
        self.install();(self.dest/'references/providers/notion.md').unlink()
        result=self.engine().inspect(self.dest)
        self.assertFalse(result['complete'])

    def test_corrupt_zip_is_actionable_without_traceback(self):
        self.archive.write_bytes(b'not a zip')
        with self.assertRaises(ValueError):self.install()

    def test_existing_ancestor_course_is_not_an_install_destination(self):
        import omni_core as c
        course=self.root/'course';c.initialize(course,{'timezone':'Asia/Shanghai'},{'topic':'x','days':[{'day':1,'topic':'x'}]})
        target=course/'skills/omni-learning-anything';sha=hashlib.sha256(self.archive.read_bytes()).hexdigest()
        with self.assertRaises(ValueError):self.engine().install(self.archive,target,sha)
        self.assertFalse(target.exists())

    def test_exact_legacy_zip_can_be_adopted_before_safe_upgrade(self):
        s=self.engine();self.dest.mkdir(parents=True)
        with ZipFile(self.archive) as z:
            for name in z.namelist():
                p=self.dest/name.split('/',1)[1];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(name))
        sha=hashlib.sha256(self.archive.read_bytes()).hexdigest()
        result=s.adopt(self.archive,self.dest,sha)
        self.assertEqual(result['action'],'adopted');self.assertTrue(s.inspect(self.dest)['integrity_verified'])
        self.assertEqual(s.install(self.archive,self.dest,sha,update=True)['action'],'unchanged')

    def test_legacy_adoption_never_accepts_modified_local_files(self):
        self.install();(self.dest/'.omni-install.json').unlink();(self.dest/'references/setup.md').write_text('mine')
        with self.assertRaises(ValueError):self.engine().adopt(self.archive,self.dest,hashlib.sha256(self.archive.read_bytes()).hexdigest())
        self.assertFalse((self.dest/'.omni-install.json').exists())

    def test_ctrl_c_during_replacement_restores_original_install(self):
        self.install();s=self.engine();before=(self.dest/'SKILL.md').read_bytes()
        updated=self.root/'new.zip';sha=self.make_zip(updated,lambda files:files.update({'references/setup.md':b'updated'}))
        original=s.os.replace
        def replace(a,b):
            if Path(a).name=='bundle' and Path(b)==self.dest.resolve():raise KeyboardInterrupt()
            return original(a,b)
        with patch.object(s.os,'replace',side_effect=replace):
            with self.assertRaises(KeyboardInterrupt):s.install(updated,self.dest,sha,update=True)
        self.assertTrue(self.dest.exists());self.assertEqual((self.dest/'SKILL.md').read_bytes(),before)
        self.assertTrue(s.inspect(self.dest)['integrity_verified'])
