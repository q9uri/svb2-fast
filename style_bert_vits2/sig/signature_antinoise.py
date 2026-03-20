#q9uri lgpl3 license
import numpy as np

def remove_voice(input_audio: np.ndarray, key:str, fs:int = 44100) -> tuple[np.ndarray, int]:
    base_audio = input_audio
    interval = 0.1
    unit_duration = interval / 12
    t_unit = np.linspace(0, unit_duration, int(fs * unit_duration), endpoint=False)

    window = np.hanning(len(t_unit))

    freqs = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'bit1': 15000.00, 'bit0': 14000.00
    }
    def gen_unit(freq):
        return 0.01 * np.sin(2 * np.pi * freq * t_unit) * window

    def gen_unit_bit(freq):
        return 0.01 * np.sin(2 * np.pi * freq * t_unit) * window

    def encode_byte(hex_val):
        binary_str = f"{int(hex_val, 16):08b}"
        seq = [gen_unit(freqs[f]) for f in ['C4', 'D4', 'E4', 'F4']]
        for bit in binary_str:
            f = freqs['bit1'] if bit == '1' else freqs['bit0']
            seq.append(gen_unit_bit(f))
        return np.concatenate(seq)

    # 埋め込みたいテキストをバイト列に変換
    text = key
    data_bytes = text.encode("ascii")

    data_with_separator = data_bytes
    hex_list = [f"{b:02x}" for b in data_with_separator]

    output_audio = base_audio.copy()

    # ベース音声の最後までループ
    # idx: 埋め込み位置のカウント
    # data_idx: hex_listのどこを読み込むかのカウント
    idx = 0
    while True:
        data_idx = idx % len(hex_list)  # データの末尾に達したら最初に戻る
        byte_hex = hex_list[data_idx]

        signal = encode_byte(byte_hex)
        start_sample = int(idx * interval * fs)
        end_sample = start_sample + len(signal)

        # 音声の終端を超えたら終了
        if end_sample > len(output_audio):
            break

        output_audio[start_sample:end_sample] -= signal
        idx += 1

    finaly_out = base_audio.copy() - output_audio.copy()

    return finaly_out, fs
