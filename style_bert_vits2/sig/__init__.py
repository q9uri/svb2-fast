# q9uri lgpl3 license
import numpy as np

from .decode import *
from .encode import *
from .sig_audioseal import SigAudioSeal
from .sig_wavmark import SigWavmark


class TriSigAudio:
    def __init__(self):
        self._wavmark_model = SigWavmark()
        self._audioseal_model = SigAudioSeal()

    def sig_audio(
        self, base_audio: np.ndarray, key: str, fs=44100
    ) -> tuple[np.ndarray, int | float]:
        output_audio, fs = sig_audio(base_audio=base_audio, key=key, fs=fs)

        try:
            output_audio, fs = self._wavmark_model.crate_sig_audio(
                audio=output_audio, key=key, sr=fs
            )
        except Exception as e:
            print(f"wavmarkでエラーが発生しました: {e}")

        try:
            output_audio, fs = self._audioseal_model.crate_sig_audio(
                audio=output_audio, key=key, sr=fs
            )

        except Exception as e:
            print(f"audiosealでしエラーが発生しました: {e}")

        return output_audio, fs

    def decode_sig(self, input_audio: np.ndarray, fs: int | float):
        decode_codebase = decode_sig(input_audio=input_audio, fs=fs)
        decode_wavmark = self._wavmark_model.decode_audio(audio=input_audio, sr=fs)
        decode_audioseal = self._audioseal_model.decode_audio(audio=input_audio, sr=fs)

        return decode_codebase, decode_wavmark, decode_audioseal
