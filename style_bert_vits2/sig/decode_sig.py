#q9uri lgpl3 license
import numpy as np
import librosa

def decode_sig(audio:np.ndarray, fs = 44100):

    interval = 0.1
    unit_samples = int(fs * (interval / 12))

    f_header = [261.63, 293.66, 329.63, 349.23]
    f_low, f_high = 14000.00, 15000.00

    #y, _ = librosa.load('./embedded_output.wav', sr=fs)
    y = audio
    decoded_results = []
    i = 0
    # 信号が短いので、1/2ユニットずつ細かくスライドしてヘッダーを探す
    step_size = unit_samples // 2

    while i < len(y) - (unit_samples * 12):
        # ヘッダー検知
        match_count = 0
        for s in range(4):
            seg = y[i + s * unit_samples: i + (s + 1) * unit_samples]
            # 短い信号なので n_fft は小さめの 512~1024
            spec = np.abs(np.fft.rfft(seg, n=2048))
            freqs_axis = np.fft.rfftfreq(2048, d=1 / fs)
            detected = freqs_axis[np.argmax(spec)]

            if abs(detected - f_header[s]) < 16:  # 誤差許容
                match_count += 1

        if match_count >= 3:  # 4音中3音合致で検知（ノイズ対策）
            data_start = i + (4 * unit_samples)
            bits = ""
            for b in range(8):
                seg = y[data_start + b * unit_samples: data_start + (b + 1) * unit_samples]
                spec = np.abs(np.fft.rfft(seg, n=2048))
                v_low = spec[np.argmin(np.abs(freqs_axis - f_low))]
                v_high = spec[np.argmin(np.abs(freqs_axis - f_high))]
                bits += "1" if v_high > v_low else "0"

            decoded_results.append(f"{int(bits, 2):02X}")
            i += int(interval * fs)  # 次のインターバルまでスキップ
        else:
            i += step_size

    return bytes.fromhex(''.join(decoded_results)).decode("ascii", "ignore")
