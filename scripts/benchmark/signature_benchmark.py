"""
Usage: .venv/bin/python -m scripts.benchmark.signature_benchmark [--device cuda] [--model koharune-ami] [--runs 3]

このスクリプトは署名の音声ごとの相性を調べるため音声を生成し署名をチェックする
測定時の推論処理はすべて FP16 で行う。

測定項目:
- 初回チャンク生成までの時間（ストリーミング版のレイテンシ）
- 全音声生成完了までの時間（総処理時間）
- 生成音声の長さごとの効果の変化
"""

import argparse
import time
from typing import Any, cast

import numpy as np
import torch
from numpy.typing import NDArray

from style_bert_vits2.constants import (
    DEFAULT_LENGTH,
    DEFAULT_NOISE,
    DEFAULT_NOISEW,
    DEFAULT_SDP_RATIO,
    Languages,
)
from style_bert_vits2.logging import logger
from style_bert_vits2.models.infer import infer, infer_stream
from style_bert_vits2.tts_model import TTSModel, TTSModelHolder
from style_bert_vits2.utils.paths import get_paths_config
from style_bert_vits2.sig.decode_sig import decode_sig

from ..utils import save_benchmark_audio, set_random_seeds


# 測定用サンプルテキスト
BENCHMARK_TEXTS = [
    {
        # 初回ロード用（ダミー）
        "text": "あああ",
        "estimated_duration": 1.1,
        "description": "短文（約1秒）",
    },
    {
        "text": "こんにちは",
        "estimated_duration": 1.1,
        "description": "短文（約1秒）",
    },
]


def measure_infer_performance(
    model: TTSModel,
    text: str,
    **infer_kwargs: Any,
) -> tuple[float, float, NDArray[np.float32], str]:
    """
    通常の infer() 関数のパフォーマンスを測定する。

    Returns:
        tuple: (総処理時間, 生成音声長(秒), 音声データ)
    """
    start_time = time.perf_counter()

    net_g = model.net_g
    assert net_g is not None

    style_vec = model.get_style_vector(0, 1.0)  # デフォルトスタイル

    # 比較のために低レベル API で推論を実行
    with torch.inference_mode():
        audio_data = infer(
            text=text,
            style_vec=style_vec,
            sdp_ratio=DEFAULT_SDP_RATIO,
            noise_scale=DEFAULT_NOISE,
            noise_scale_w=DEFAULT_NOISEW,
            length_scale=DEFAULT_LENGTH,
            sid=0,
            language=Languages.JP,
            hps=model.hyper_parameters,
            net_g=net_g,
            device=model.device,
            **infer_kwargs,
        )

        end_time = time.perf_counter()
        total_time = end_time - start_time

        # 生成音声の長さを計算
        audio_duration = len(audio_data) / model.hyper_parameters.data.sampling_rate
        decoded_text = decode_sig(audio_data, model.hyper_parameters.data.sampling_rate)

        return total_time, audio_duration, audio_data, decoded_text


def run_benchmark(
    device: str = "cpu",
    model_name: str = "koharune-ami",
    num_runs: int = 3,
    use_fp16: bool = True,
    fix_seed: bool = False,
) -> None:
    """
    ベンチマークを実行する。
    """
    # ランダムシード固定
    if fix_seed:
        set_random_seeds()

    print("=" * 80)
    print("Style-Bert-VITS2 ストリーミング推論パフォーマンス測定")
    print("=" * 80)
    print(f"デバイス: {device}")
    print(f"モデル: {model_name}")
    print(f"測定回数: {num_runs}")
    print(f"FP16: {use_fp16}")
    print(f"ランダムシード固定: {'有効' if fix_seed else '無効'}")
    print("=" * 80)

    # モデルホルダーを初期化
    model_holder = TTSModelHolder(
        get_paths_config().assets_root,
        device,
        onnx_providers=[],
        ignore_onnx=True,
        use_fp16=use_fp16,
    )
    if len(model_holder.models_info) == 0:
        print("エラー: 音声合成モデルが見つかりませんでした。")
        return

    # 指定されたモデルを検索
    model_info = None
    for info in model_holder.models_info:
        if info.name == model_name:
            model_info = info
            break

    if model_info is None:
        print(f'エラー: モデル "{model_name}" が見つかりませんでした。')
        print("利用可能なモデル:")
        for info in model_holder.models_info:
            print(f"  - {info.name}")
        return

    # Safetensors 形式のモデルファイルを検索
    model_files = [
        f
        for f in model_info.files
        if f.endswith(".safetensors") and not f.startswith(".")
    ]
    if len(model_files) == 0:
        print(
            f'エラー: モデル "{model_name}" の .safetensors ファイルが見つかりませんでした。'
        )
        return

    model_file = model_files[0]
    print(f"使用するモデルファイル: {model_file}")
    print()

    # モデルをロード
    model = model_holder.get_model(model_name, model_file)
    model.load()

    # 結果を保存するリスト
    results = []

    # 各テキストでベンチマークを実行
    for i, test_case in enumerate(BENCHMARK_TEXTS):
        text = cast(str, test_case["text"])
        estimated_duration = test_case["estimated_duration"]
        description = test_case["description"]

        print(f"測定中: {description}")
        print(f"テキスト: {text}")

        # 複数回実行して平均を取る
        infer_times = []
        infer_durations = []
        infer_decoded_text = []

        # 最後の実行の音声データを保存用に記録
        last_normal_audio = None
        last_sample_rate = None

        for run in range(num_runs):
            try:
                # 通常の infer() を測定
                infer_time, infer_duration, normal_audio, decoded_text= measure_infer_performance(
                    model,
                    text,
                    use_fp16=use_fp16,
                    clear_cuda_cache=True,
                )
                infer_times.append(infer_time)
                infer_durations.append(infer_duration)
                infer_decoded_text.append(decoded_text)

                # 最後の実行の音声データを保存
                if run == num_runs - 1:
                    last_normal_audio = normal_audio
                    last_sample_rate = model.hyper_parameters.data.sampling_rate

            except Exception as ex:
                logger.exception(f"測定中にエラーが発生しました: {ex}")
                continue

        if not infer_times:
            print("  測定に失敗しました。")
            continue

        # 初回はロードが入るため捨てる
        if i == 0:
            continue

        # 音声ファイルを保存（初回のダミーは除く）
        if (
            i > 0  # 初回はダミー
            and last_normal_audio is not None
            and last_sample_rate is not None
        ):
            save_benchmark_audio(
                last_normal_audio,
                last_sample_rate,
                text,
                "signature_benchmark",
                "",
            )

        result = {
            "text": text,
            "description": description,
            "estimated_duration": estimated_duration,
            "decoded_text": infer_decoded_text,
        }
        results.append(result)

        # 個別結果を表示
        for decoded_text in result['decoded_text']:
            print(f"デコード結果: {decoded_text}")
        print("\n")

    # モデルをアンロード
    model.unload()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Style-Bert-VITS2 ストリーミング推論パフォーマンス測定"
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "cuda"],
        help="推論に使用するデバイス (default: cpu)",
    )
    parser.add_argument(
        "--model",
        default="koharune-ami",
        help="使用するモデル名 (default: koharune-ami)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="各テストケースの実行回数 (default: 3)",
    )
    parser.add_argument(
        "--fp16",
        dest="use_fp16",
        action="store_true",
        help="FP16 で推論を行う (default)",
    )
    parser.add_argument(
        "--no-fp16",
        dest="use_fp16",
        action="store_false",
        help="FP16 を無効化する",
    )
    parser.add_argument(
        "--fix-seed",
        action="store_true",
        help="ランダムシードを固定して再現性を確保する",
    )
    parser.set_defaults(use_fp16=True)

    args = parser.parse_args()

    try:
        run_benchmark(
            device=args.device,
            model_name=args.model,
            num_runs=args.runs,
            use_fp16=args.use_fp16,
            fix_seed=args.fix_seed,
        )
    except KeyboardInterrupt:
        print("\nベンチマークが中断されました。")
    except Exception as ex:
        logger.exception(f"ベンチマーク実行中にエラーが発生しました: {ex}")


if __name__ == "__main__":
    main()
