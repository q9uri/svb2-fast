import librosa
import numpy as np
import torch
from audioseal import AudioSeal


class SigAudioSeal:
    def __init__(self):
        self.model = AudioSeal.load_generator("audioseal_wm_16bits")
        self.model.eval()
        self.detector = AudioSeal.load_detector("audioseal_detector_16bits")

    def __set_audio_size(self, target_audio: np.ndarray, input_output: np.ndarray):
        # audio の長さでスライス。もし足りなければ 0 で埋める（念のため）
        if len(input_output) < len(target_audio):
            input_output = np.pad(
                input_output, (0, len(target_audio) - len(input_output))
            )
        else:
            input_output = input_output[: len(target_audio)]

        return input_output

    def crate_sig_audio(self, audio: np.ndarray, key: str, sr: int | float):
        audio_16k = librosa.resample(audio, orig_sr=sr, target_sr=16000)

        tmp_audio_without_16khz = librosa.resample(
            audio_16k, orig_sr=16000, target_sr=sr
        )
        tmp_audio_without_16khz = self.__set_audio_size(audio, tmp_audio_without_16khz)
        audio_without_16khz = audio - tmp_audio_without_16khz

        # 2. torch.Tensorに変換
        # librosaはfloat32なので、そのまま変換してOKです
        audio_16k = torch.from_numpy(audio_16k).clone()

        # 3. torchaudio形式 (L, C) -> (C, L) への調整
        # librosaでモノラル読み込みした場合、(Samples,) なので (1, Samples) に拡張します
        if audio_16k.ndim == 1:
            audio_16k = audio_16k.unsqueeze(0)

        # 2. バッチ次元の追加 ★これが重要
        # AudioSeal が要求する (Batch, Channels, Time) の形にする
        audio_16k = audio_16k.unsqueeze(0)  # (1, Samples) -> (1, 1, Samples)

        data_bytes = key.encode("ascii")
        data_with_separator = data_bytes
        hex_list = [f"{b:02x}" for b in data_with_separator]

        payload = []
        for hex_val in hex_list:
            binary_str = f"{int(hex_val, 16):08b}"
            for bit in binary_str:
                if bit == "0":
                    payload.append(0)
                elif bit == "1":
                    payload.append(1)

        msg = torch.tensor(payload, dtype=torch.long).unsqueeze(0).to(audio_16k.device)

        watermark = self.model.get_watermark(audio_16k, 16000, msg)
        watermarked_audio = audio_16k + watermark
        watermarked_audio = (
            watermarked_audio.to("cpu").detach().squeeze().numpy().copy()
        )

        tmp_watermarked_audio_44khz = librosa.resample(
            watermarked_audio, orig_sr=16000, target_sr=sr
        )

        tmp_watermarked_audio_44khz = self.__set_audio_size(
            audio_without_16khz, tmp_watermarked_audio_44khz
        )
        watermarked_audio_44khz = audio_without_16khz + tmp_watermarked_audio_44khz

        return watermarked_audio_44khz, sr

    def decode_audio(self, audio: np.ndarray, sr: int):
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

        # 2. torch.Tensorに変換
        # librosaはfloat32なので、そのまま変換してOKです
        audio = torch.from_numpy(audio).clone()

        # 3. torchaudio形式 (L, C) -> (C, L) への調整
        # librosaでモノラル読み込みした場合、(Samples,) なので (1, Samples) に拡張します
        if audio.ndim == 1:
            audio = audio.unsqueeze(0)

        # 2. バッチ次元の追加 ★これが重要
        # AudioSeal が要求する (Batch, Channels, Time) の形にする
        audio = audio.unsqueeze(0)  # (1, Samples) -> (1, 1, Samples)

        result, message = self.detector.detect_watermark(audio)

        data = message[0].tolist()
        if data is None:
            return ""

        cur_bits = ""
        decoded_results = []
        for i, bit in enumerate(data, start=1):
            cur_bits += str(bit)
            if i % 8 == 0:
                decoded_results.append(f"{int(cur_bits, 2):02X}")
                cur_bits = ""

        return bytes.fromhex("".join(decoded_results)).decode("ascii", "ignore")
