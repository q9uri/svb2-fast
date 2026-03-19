#Usage: .venv/bin/python -m scripts.sig.enable_sig

from pathlib import Path
import librosa
from style_bert_vits2.sig import sig_audio
import soundfile as sf

input_dir = Path(__file__).parent / "wavs/input"
output_dir = Path(__file__).parent / "wavs/output"

def is_audio_file(file: Path) -> bool:
    supported_extensions = [".wav", ".flac", ".mp3", ".ogg", ".opus", ".m4a"]
    return file.suffix.lower() in supported_extensions

audio_files = [file for file in input_dir.rglob("*") if is_audio_file(file)]

for audio_file in audio_files:
    audio, sr = librosa.load(str(audio_file), sr=None, mono=False)

    audio, sr = sig_audio(audio, sr)
    sf.write(str(output_dir / f"{audio_file.name}.wav"), audio, sr)