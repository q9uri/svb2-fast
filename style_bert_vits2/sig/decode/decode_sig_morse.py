#q9uri lgpl3 license
import numpy as np

def decode_sig_morse(audio:np.ndarray, fs = 44100):
    # --- 設定 ---
    unit_duration = 0.05
    samples_per_unit = int(fs * unit_duration)
    freq_dot = 440.0
    freq_spacer = 660.0
    freq_code_spacer = 1320.0
    freq_dash = 880.0
    freq_header = 1760.0

    threshold = 0.05

    MORSE_TO_CHAR = {v: k for k, v in
                     {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                      'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                      'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                      'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
                      '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', '/': ' '}.items()}
    MORSE_TO_CHAR['/'] = ' '

    #y, _ = librosa.load('./morse_sync_output.wav', sr=fs)
    y = audio

    # 1. 相互相関用のヘッダーテンプレートを作成
    header_template = np.linspace(0, 0.1, int(fs * 0.1), endpoint=False)
    header_template = 0.1 * np.sin(2 * np.pi * freq_header * header_template) * np.hanning(len(header_template))

    # 2. 相互相関の計算（波形の一致度を探す）
    # 全体だと重いので、最初の1セット分（例: 2秒間）をスキャン
    scan_len = int(fs * 2.0)
    correlation = np.correlate(y[:scan_len], header_template, mode='valid')
    header_start_sample = np.argmax(correlation)  # 最も一致したサンプル位置

    print(f"Header Sync OK! Found at sample: {header_start_sample} ({header_start_sample / fs:.3f}s)")

    # 3. データの読み取り開始位置を決定
    # ヘッダー(0.1s) + ガード無音(0.1s) の直後から読み取る
    data_start_idx = header_start_sample + int(fs * 0.1) + int(fs * 0.1)

    symbols = ""
    consecutive_silence = 0
    i = data_start_idx

    while i < len(y) - samples_per_unit:
        seg = y[i: i + samples_per_unit]
        spec = np.abs(np.fft.rfft(seg, n=2048))
        freqs_axis = np.fft.rfftfreq(2048, d=1 / fs)

        idx_dot = np.argmin(np.abs(freqs_axis - freq_dot))
        idx_dash = np.argmin(np.abs(freqs_axis - freq_dash))
        idx_spacer = np.argmin(np.abs(freqs_axis - freq_spacer))
        idx_code_spacer = np.argmin(np.abs(freqs_axis - freq_code_spacer))

        amp_dot = spec[idx_dot]
        amp_dash = spec[idx_dash]
        amp_spacer = spec[idx_spacer]
        amp_code_spacer = spec[idx_code_spacer]

        current_max = max(amp_dot, amp_dash, amp_spacer, amp_code_spacer)

        if current_max < threshold:
            # そもそも音が小さすぎる場合は本当の無音
            consecutive_silence += 1
        elif amp_dot == current_max:
            symbols += "."
            consecutive_silence = 0
        elif amp_dash == current_max:
            symbols += "-"
            consecutive_silence = 0
        elif amp_code_spacer == current_max:
            # コードスペーサーが鳴っている間は「文字の継続中」なので、
            # 記号としてカウントせず、かつ無音カウントも増やさない
            pass
        else:
            # amp_spacer が一番強い場合は「意図的なスペース」
            consecutive_silence += 1
            if consecutive_silence == 3:
                symbols += " "
            elif consecutive_silence == 7:
                symbols += " / "
            if consecutive_silence > 20: break  # 長すぎる無音で終了

        i += samples_per_unit

    # デコード結果表示
    decoded_text = "".join([MORSE_TO_CHAR.get(p, "") for p in symbols.split(" ") if p])
    return decoded_text