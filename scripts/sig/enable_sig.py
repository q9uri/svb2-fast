# Usage: .venv/bin/python -m scripts.sig.enable_sig

from pathlib import Path

import librosa
import soundfile as sf

from style_bert_vits2.sig import TriSigAudio, sig_audio_morse


input_dir = Path(__file__).parent / "wavs/input"
output_dir = Path(__file__).parent / "wavs/output"
output_morse_dir = Path(__file__).parent / "wavs/output_morse"


def is_audio_file(file: Path) -> bool:
    supported_extensions = [".wav", ".flac", ".mp3", ".ogg", ".opus", ".m4a"]
    return file.suffix.lower() in supported_extensions


audio_files = [file for file in input_dir.rglob("*") if is_audio_file(file)]

for audio_file in audio_files:
    trisig = TriSigAudio()
    audio, sr = librosa.load(str(audio_file), sr=None, mono=False)
    audio, sr = trisig.sig_audio(base_audio=audio, key="ai", fs=sr)

    sf.write(str(output_dir / f"{audio_file.name}.wav"), audio, sr)

for audio_file in audio_files:
    audio, sr = librosa.load(str(audio_file), sr=None, mono=False)

    audio, sr = sig_audio_morse(base_audio=audio, key="BY AI", fs=sr)
    sf.write(str(output_morse_dir / f"{audio_file.name}_morse.wav"), audio, sr)
