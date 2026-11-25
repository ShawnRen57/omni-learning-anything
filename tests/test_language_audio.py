import sys
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills/omni-learning-anything/scripts'))
import omni_language_audio as audio


class AudioTests(unittest.TestCase):
    def test_voice_region_and_language_match(self):
        voices = [('Kyoko', 'ja-jp'), ('Ava', 'en-us')]
        self.assertEqual(audio._voice(voices, 'ja'), voices[0])
        with self.assertRaisesRegex(ValueError, 'No installed voice'):
            audio._voice(voices, 'en-gb')

    def test_failed_generation_preserves_files_and_verified_track_can_be_reused(self):
        def speech(locale, text, target):
            with wave.open(str(target), 'wb') as stream:
                stream.setparams((1, 2, 8000, 0, 'NONE', 'PCM'))
                stream.writeframes(b'\x01\x10' * 8000)
            return 'fixture', 'fixture', locale

        with tempfile.TemporaryDirectory() as tmp, patch.object(audio, '_synthesize', side_effect=speech):
            root = Path(tmp)
            def make(name): return audio.generate(root, 'ja-JP', 'どうぞ。', name)
            with self.assertRaises(ValueError): make('../wrong.wav')
            report = make('audio/cue.wav')
            self.assertEqual(make('audio/cue.wav'), report)
            self.assertEqual(report['duration_seconds'], 1.0)
            track = root / report['path']
            track.write_bytes(b'earlier recording')
            with self.assertRaisesRegex(ValueError, 'different recording'): make('audio/cue.wav')
            self.assertEqual(track.read_bytes(), b'earlier recording')
