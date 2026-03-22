import librosa
import numpy as np
import torch
import wavmark


class SigWavmark:
    def __init__(self):
        # 1.load model
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = wavmark.load_model().to(device)

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
        # 2.create 16-bit payload
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

        audio_16k = librosa.resample(audio, orig_sr=sr, target_sr=16000)

        tmp_audio_without_16khz = librosa.resample(
            audio_16k, orig_sr=16000, target_sr=sr
        )

        tmp_audio_without_16khz = self.__set_audio_size(audio, tmp_audio_without_16khz)
        audio_without_16khz = audio - tmp_audio_without_16khz

        watermarked_audio, _ = wavmark.encode_watermark(
            self.model, audio_16k, payload, show_progress=True
        )
        tmp_watermarked_audio_44khz = librosa.resample(
            watermarked_audio, orig_sr=16000, target_sr=sr
        )
        tmp_watermarked_audio_44khz = self.__set_audio_size(
            tmp_audio_without_16khz, tmp_watermarked_audio_44khz
        )
        watermarked_audio_44khz = audio_without_16khz + tmp_watermarked_audio_44khz

        return watermarked_audio_44khz, sr

    def decode_audio(self, audio: np.ndarray, sr: int):
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

        payload = wavmark.decode_watermark(self.model, audio, show_progress=True)

        data = payload[0]
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
