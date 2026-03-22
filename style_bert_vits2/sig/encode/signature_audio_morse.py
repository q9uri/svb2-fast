# q9uri lgpl3 license
import numpy as np


def sig_audio_morse(
    base_audio: np.ndarray, key: str, fs=44100
) -> tuple[np.ndarray, int]:
    # --- 設定 ---
    unit_duration = 0.05
    freq_dot = 440.0
    freq_spacer = 660.0
    freq_code_spacer = 1320.0
    freq_dash = 880.0
    freq_header = 1760.0

    amplitude = 0.5

    MORSE_CODE_DICT = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "0": "-----",
        " ": "/",
    }

    def gen_element(duration, freq=None):
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        if freq is not None:
            return amplitude * np.sin(2 * np.pi * freq * t) * np.hanning(len(t))
        return np.zeros(len(t))

    def text_to_morse_signal(text):
        full_signal = []
        for char in text.upper():
            if char in MORSE_CODE_DICT:
                code = MORSE_CODE_DICT[char]
                for i, symbol in enumerate(code):
                    f = freq_dot if symbol == "." else freq_dash
                    full_signal.append(gen_element(unit_duration, freq=f))
                    if i < len(code) - 1:
                        # 記号間をアイドル周波数で埋める
                        full_signal.append(
                            gen_element(unit_duration, freq=freq_code_spacer)
                        )
                # 文字間をアイドル周波数で埋める
                full_signal.append(gen_element(unit_duration * 3, freq=freq_spacer))
        return np.concatenate(full_signal)

    # ヘッダー（0.1秒）
    header_signal = gen_element(0.1, freq=freq_header)
    # ガード区間（無音）
    gap = gen_element(0.1, freq=None)
    # モールス信号
    body_signal = text_to_morse_signal(key)

    # 1セット: [ヘッダー] + [無音] + [モールス] + [末尾無音]
    loop_unit = np.concatenate(
        [
            header_signal,
            gap,
            body_signal,
            gen_element(unit_duration * 7, freq=freq_spacer),
        ]
    )

    num_loops = int(np.ceil(len(base_audio) / len(loop_unit)))
    repeated_signal = np.tile(loop_unit, num_loops)[: len(base_audio)]
    output_audio = base_audio + repeated_signal

    return output_audio, fs
