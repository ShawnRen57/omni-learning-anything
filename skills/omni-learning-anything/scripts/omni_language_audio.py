"""Produce a private listening track with an installed local speech engine."""
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import wave


def configure(sub):
    command = sub.add_parser('language-audio', help='Generate an optional local WAV listening track')
    command.add_argument('--locale', required=True, help='Target voice locale, e.g. ja-JP')
    command.add_argument('--text', required=True, help='Plain text in the target language')
    command.add_argument('--output', required=True, help='New WAV filename relative to the course')


def _run(args, text=None):
    try:
        return subprocess.run(args, input=text, text=True, capture_output=True, check=True,
                              encoding='utf-8', timeout=90).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        raise ValueError('Local speech engine failed. Check the selected voice or use a sourced recording.') from error


def _voice(available, locale):
    matches = [(voice, tag) for voice, tag in available if tag == locale or
               ('-' not in locale and tag.split('-')[0] == locale)]
    if not matches:
        raise ValueError(f'No installed voice for {locale}. Use a sourced recording or select an installed target locale.')
    # Prefer a system's plain voices over novelty or character voices when available.
    ordinary = {'kyoko', 'samantha', 'thomas', 'anna', 'monica', 'meijia', 'tingting', 'yuna', 'luciana'}
    return next((v for v in matches if v[0].casefold() in ordinary), matches[0])


def _synthesize(locale, text, path):
    say = shutil.which('say') if sys.platform == 'darwin' else None
    if say:
        voices = re.findall(r'^(.+?)\s+([a-z]{2,3}_[A-Za-z_]+)\s+#', _run([say, '-v', '?']), re.M)
        voice, actual = _voice([(v.strip(), tag.lower().replace('_', '-')) for v, tag in voices], locale)
        _run([say, '-v', voice, '-o', str(path), '--file-format=WAVE', '--data-format=LEI16@22050', '-f', '-'], text)
        return 'say', voice, actual
    engine = shutil.which('espeak-ng')
    if engine:
        voices = []
        for line in _run([engine, '--voices']).splitlines():
            fields = line.split()
            if len(fields) > 4 and fields[0].isdigit():
                voices.append((fields[1], fields[1].lower()))
        voice, actual = _voice(voices, locale)
        _run([engine, '-b', '1', '-v', voice, '-w', str(path), '--stdin'], text)
        return 'espeak-ng', voice, actual
    raise ValueError('No local speech engine available. Use an accessible target-language recording, or install eSpeak NG with the requested voice.')


def generate(root, locale, text, output):
    root = Path(root).resolve()
    relative = Path(output)
    if (relative.is_absolute() or '..' in relative.parts or relative.suffix.lower() != '.wav'
            or not (root / relative).resolve().is_relative_to(root)):
        raise ValueError('Choose a WAV filename inside the course archive.')
    if not re.fullmatch(r'[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*', locale):
        raise ValueError('Provide a voice locale such as ja-JP.')
    if not text.strip() or len(text) > 2000 or '[[' in text or any(ord(c) < 32 and c not in '\r\n\t' for c in text):
        raise ValueError('Supply 1–2000 characters of plain target-language speech.')
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink():
        raise ValueError('Choose an audio output without a symbolic link.')
    with tempfile.TemporaryDirectory(dir=target.parent) as tmp:
        track = Path(tmp) / 'track.wav'
        engine, voice, actual = _synthesize(locale.lower(), text, track)
        try:
            with wave.open(str(track), 'rb') as wav:
                frames = wav.readframes(wav.getnframes())
                if not any(frames) or len(frames) != wav.getnframes() * wav.getsampwidth() * wav.getnchannels():
                    raise ValueError('Speech engine produced an empty, silent or incomplete audio track.')
                duration = round(wav.getnframes() / wav.getframerate(), 2)
        except (wave.Error, EOFError) as error:
            raise ValueError('Speech engine produced an unreadable WAV file.') from error
        contents = track.read_bytes()
        track.chmod(0o600)
        try:
            os.link(track, target)
        except FileExistsError:
            if target.read_bytes() != contents:
                raise ValueError('A different recording already exists at that path. Choose a new filename.') from None
    return {'path': relative.as_posix(), 'kind': 'synthesized', 'voice': voice, 'locale': actual,
            'engine': engine, 'duration_seconds': duration, 'sha256': hashlib.sha256(contents).hexdigest()}
