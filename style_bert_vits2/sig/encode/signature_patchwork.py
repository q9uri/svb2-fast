import numpy as np
import scipy.fftpack as fft


def embed_watermark(audio_segment:np.ndarray, bit:int, secret_key_hash:bytes, sr: int=44100):
    """
    audio_segment: float32のモノラル波形 (FFTサイズ分, 例: 2048 samples)
    bit: 埋め込む値 (0 or 1)
    secret_key_hash: SHA-256ハッシュのバイト列
    """
    # 1. 周波数ドメインへ変換
    spec = fft.fft(audio_segment)
    magnitudes = np.abs(spec)
    phases = np.angle(spec)

    # 2. ハッシュから周波数ペアを選択 (例: 1kHz - 6kHzの範囲)
    # 簡易的にハッシュの特定バイトからインデックスを算出
    f_min, f_max = 1000, 6000
    bin_min = int(f_min * len(audio_segment) / sr)
    bin_max = int(f_max * len(audio_segment) / sr)

    # 鍵に基づいてペア(A, B)を複数選ぶ（統計的堅牢性のため）
    np.random.seed(int.from_bytes(secret_key_hash[:4], 'big'))
    pairs = []
    for _ in range(16):  # 1ビットを16ペアに分散
        idx_a = np.random.randint(bin_min, bin_max)
        idx_b = idx_a + np.random.randint(1, 10)  # 近接周波数を選ぶ
        pairs.append((idx_a, idx_b))

    # 3. エネルギーの微調整 (Patchwork)
    alpha = 0.05  # 変化の強さ (DNSMOS 4.0維持ならこれくらい微小から開始)

    for idx_a, idx_b in pairs:
        # 相対的なエネルギー差を作る
        avg = (magnitudes[idx_a] + magnitudes[idx_b]) / 2
        if bit == 1:
            magnitudes[idx_a] = avg * (1 + alpha)
            magnitudes[idx_b] = avg * (1 - alpha)
        else:
            magnitudes[idx_a] = avg * (1 - alpha)
            magnitudes[idx_b] = avg * (1 + alpha)

    # 4. 時間ドメインに戻す
    new_spec = magnitudes * np.exp(1j * phases)
    new_audio = fft.ifft(new_spec).real

    return new_audio.astype(np.float32)


import hashlib

def get_key_hash(key: str) -> bytes:
    """鍵をSHA-256でハッシュ化"""
    return hashlib.sha256(key.encode('utf-8')).digest()

def process_block_patchwork(audio_segment: np.ndarray, bit: int, key_hash: bytes, sr: int, alpha: float = 0.05):
    """
    ブロック単位でパッチワーク埋め込みを行う核となる関数
    """
    # 1. 周波数ドメインへ変換
    spec = fft.fft(audio_segment)
    magnitudes = np.abs(spec)
    phases = np.angle(spec)

    # 2. ハッシュから周波数ペアを選択 (1kHz - 8kHz: 圧縮に強く耳に付きにくい帯域)
    f_min, f_max = 1000, 8000
    bin_min = int(f_min * len(audio_segment) / sr)
    bin_max = int(f_max * len(audio_segment) / sr)

    # 鍵のハッシュをシードにペアを決定
    seed = int.from_bytes(key_hash[:4], 'big')
    # ビット値もシードに含めることでパターンを分散（セキュリティ向上）
    gen = np.random.RandomState(seed ^ bit)

    pairs = []
    for _ in range(16):  # 1ビットを16ペアに分散して堅牢性を確保
        idx_a = gen.randint(bin_min, bin_max)
        idx_b = idx_a + gen.randint(1, 15)
        if idx_b < len(magnitudes):
            pairs.append((idx_a, idx_b))

    # 3. エネルギーの微調整 (Patchwork)
    # alphaは元信号のエネルギーに対する比率。0.05=5%の変化
    for idx_a, idx_b in pairs:
        avg = (magnitudes[idx_a] + magnitudes[idx_b]) / 2
        if bit == 1:
            magnitudes[idx_a] = avg * (1 + alpha)
            magnitudes[idx_b] = avg * (1 - alpha)
        else:
            magnitudes[idx_a] = avg * (1 - alpha)
            magnitudes[idx_b] = avg * (1 + alpha)

    # 4. 時間ドメインに戻す
    new_spec = magnitudes * np.exp(1j * phases)
    return fft.ifft(new_spec).real.astype(np.float32)

def sig_audio_patchwork(base_audio: np.ndarray, key: str, fs=44100, alpha=0.06) -> tuple[np.ndarray, int]:
    """
    ベース音声全体に鍵に基づいた署名をループ埋め込みする
    """
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

    def embed_sync_header():
        seq = [gen_unit(freqs[f]) for f in ['C4', 'D4', 'E4', 'F4']]
        return np.concatenate(seq)

    header = embed_sync_header()
    # まずヘッダーを書き込む
    output_audio = base_audio.copy()
    output_audio[:len(header)] += header

    key_hash = get_key_hash(key)

    # 1ブロックの長さ (約46ms: 2048 samples @ 44.1kHz)
    # FFT効率と時間解像度のバランスが良いサイズ
    block_size = 2048
    hop_size = 1024 # 50%オーバーラップで繋ぎ目を滑らかにする
    window = np.hanning(block_size)

    temp_signal = np.zeros_like(base_audio)  # 埋め込み用の一時バッファ
    weight_map = np.zeros_like(base_audio)

    # 鍵をビット列に変換 (ASCII)
    data_bits = "".join(f"{b:08b}" for b in key.encode("ascii"))
    num_bits = len(data_bits)

    # 音声をブロックごとにスキャン
    for i in range(0, len(base_audio) - block_size, hop_size):
        # 現在のブロックがどのビットを担当するか
        bit_idx = (i // hop_size) % num_bits
        target_bit = int(data_bits[bit_idx])

        segment = base_audio[i:i+block_size]

        # パッチワーク埋め込み実行
        processed_segment = process_block_patchwork(segment * window, target_bit, key_hash, fs, alpha)

        # オーバーラップ加算 (OLA)
        temp_signal[i:i + block_size] += processed_segment
        #output_audio[i:i+block_size] += processed_segment
        weight_map[i:i+block_size] += window

    # ウェイトで割って正規化（窓関数の影響を相殺）
    safe_idx = weight_map > 0
    #output_audio[safe_idx] /= weight_map[safe_idx]
    output_audio[safe_idx] = temp_signal[safe_idx] / weight_map[safe_idx]

    # 元の音声が短すぎる場合の処理
    remainder = len(base_audio) - len(output_audio)
    if remainder > 0:
        output_audio = np.append(output_audio, base_audio[-remainder:])

    return output_audio, fs