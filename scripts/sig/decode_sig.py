#Usage: .venv/bin/python -m scripts.sig.enable_sig

from pathlib import Path
import librosa
from style_bert_vits2.sig import decode_sig


output_dir = Path(__file__).parent / "wavs/output"

def is_audio_file(file: Path) -> bool:
    supported_extensions = [".wav", ".flac", ".mp3", ".ogg", ".opus", ".m4a"]
    return file.suffix.lower() in supported_extensions

audio_files = [file for file in output_dir.rglob("*") if is_audio_file(file)]

def decode_text():
    decode_texts = []
    for audio_file in audio_files:
        audio, sr = librosa.load(str(audio_file), sr=None, mono=False)

        decode_text = decode_sig(audio, sr)
        decode_texts.append(f"{audio_file},{decode_text}")

    Path("./result.csv").write_text("\n".join(decode_texts), encoding="utf-8")


def decode_text_fake():
    decode_texts = []
    for audio_file in audio_files:
        audio, sr = librosa.load(str(audio_file), sr=None, mono=False)

        decode_text = decode_sig(audio, sr, True)
        decode_texts.append(f"{audio_file},{decode_text}")

    Path("./result_fake.csv").write_text("\n".join(decode_texts), encoding="utf-8")

if __name__ == "__main__":
    decode_text_fake()
    decode_text()