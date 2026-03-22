import numpy as np
import scipy.fftpack as fft
import hashlib

def extract_watermark(audio_segment:np.ndarray, secret_key_hash:bytes, sr:int=44100):
    """
    埋め込まれたビットを推定する
    """
    spec = np.abs(fft.fft(audio_segment))

    f_min, f_max = 1000, 6000
    bin_min = int(f_min * len(audio_segment) / sr)
    bin_max = int(f_max * len(audio_segment) / sr)

    np.random.seed(int.from_bytes(secret_key_hash[:4], 'big'))
    diff_sum = 0

    for _ in range(16):
        idx_a = np.random.randint(bin_min, bin_max)
        idx_b = idx_a + np.random.randint(1, 10)
        # 対数領域での差分を累計 (音量変化に強くするため)
        diff_sum += np.log(spec[idx_a] + 1e-9) - np.log(spec[idx_b] + 1e-9)

    return 1 if diff_sum > 0 else 0


def get_key_hash(key: str) -> bytes:
    return hashlib.sha256(key.encode('utf-8')).digest()


def extract_bit_from_block(audio_segment: np.ndarray, key_hash: bytes, sr: int):
    # パッチワーク法のコア（変更なし）
    spec = np.abs(fft.fft(audio_segment))
    f_min, f_max = 1000, 8000
    bin_min = int(f_min * len(audio_segment) / sr)
    bin_max = int(f_max * len(audio_segment) / sr)
    seed = int.from_bytes(key_hash[:4], 'big')

    scores = {0: 0.0, 1: 0.0}
    for hypothesis_bit in [0, 1]:
        gen = np.random.RandomState(seed ^ hypothesis_bit)
        diff_sum = 0
        for _ in range(16):
            idx_a = gen.randint(bin_min, bin_max)
            idx_b = idx_a + gen.randint(1, 15)
            if idx_b < len(spec):
                diff = np.log(spec[idx_a] + 1e-9) - np.log(spec[idx_b] + 1e-9)
                diff_sum += diff
        scores[hypothesis_bit] = diff_sum if hypothesis_bit == 1 else -diff_sum
    return 1 if scores[1] > scores[0] else 0


def decode_sig_patchwork(input_audio: np.ndarray, key: str, fs: int = 44100):
    key_hash = get_key_hash(key)
    block_size = 2048
    hop_size = 1024

    # ヘッダー検知用の設定
    interval = 0.1
    unit_samples = int(fs * (interval / 12))
    f_header = [261.63, 293.66, 329.63, 349.23]

    data_bits_expected = "".join(f"{b:08b}" for b in key.encode("ascii"))
    num_bits = len(data_bits_expected)

    i = 0
    step_size = unit_samples // 2

    # --- 同期処理 (ヘッダーを探す) ---
    found_start = -1
    while i < len(input_audio) - (unit_samples * 12):
        match_count = 0
        for s in range(4):
            seg = input_audio[i + s * unit_samples: i + (s + 1) * unit_samples]
            if len(seg) < 2048: continue
            spec = np.abs(np.fft.rfft(seg, n=2048))
            freqs_axis = np.fft.rfftfreq(2048, d=1 / fs)
            detected = freqs_axis[np.argmax(spec)]
            if abs(detected - f_header[s]) < 16:
                match_count += 1

        if match_count >= 3:
            # ヘッダー(4音)の直後をデータ開始点とする
            found_start = i + (4 * unit_samples)
            break
        i += step_size

    if found_start == -1:
        # ヘッダーが見つからない場合は先頭から試行（フォールバック）
        found_start = 0

    # --- 抽出処理 (同期点から開始) ---
    extracted_bits = []
    # 同期した位置から block_size ごとにスキャン
    for j in range(found_start, len(input_audio) - block_size, hop_size):
        segment = input_audio[j:j + block_size]
        # 窓関数を適用（埋め込み側が segment * window なので合わせる）
        window = np.hanning(block_size)
        bit = extract_bit_from_block(segment * window, key_hash, fs)
        extracted_bits.append(bit)

    if not extracted_bits:
        return ""

    # --- 多数決処理 ---
    final_bits = ""
    for b_idx in range(num_bits):
        this_bit_samples = extracted_bits[b_idx::num_bits]
        if len(this_bit_samples) > 0:
            # 統計的な平均でビットを決定
            final_bits += "1" if np.mean(this_bit_samples) > 0.5 else "0"

    try:
        decoded_bytes = []
        for k in range(0, len(final_bits), 8):
            byte_str = final_bits[k:k + 8]
            if len(byte_str) == 8:
                decoded_bytes.append(int(byte_str, 2))
        return bytes(decoded_bytes).decode("ascii", "ignore")
    except Exception:
        return ""