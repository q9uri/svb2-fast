import torch
import torch.nn as nn
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

import onnx
from onnxsim import simplify
from onnxruntime.quantization import quantize_dynamic, QuantType
from onnxruntime.quantization import shape_inference

def export():

    onnx_temp_model_path = "./bert/sse-fast-ja-onnx/model.onnx"
    onnx_fp16_model_path = "./bert/sse-fast-ja-onnx/model_fp16.onnx"
    #onnx_temp_model_path = "./bert/sse-fast-en-onnx/model.onnx"
    #onnx_fp16_model_path = "./bert/sse-fast-en-onnx/model_fp16.onnx"

    # 1. モデルのロード
    model_id = "RikkaBotan/stable-static-embedding-fast-retrieval-mrl-ja"
    #model_id = "RikkaBotan/stable-static-embedding-fast-retrieval-mrl-en"
    st_model = SentenceTransformer(model_id, trust_remote_code=True)
    sse_module = st_model[0]

    class SSEForVITS2(nn.Module):
        def __init__(self, sse):
            super().__init__()
            # EmbeddingBag ではなく、2次元入力に対応した通常の Embedding に差し替え
            self.emb = nn.Embedding.from_pretrained(sse.embedding.weight)
            self.dyt = sse.dyt
            # 512 -> 1024 次元へのアップサイクル層
            self.upcycle_proj = nn.Linear(512, 1024)

        def forward(self, input_ids, attention_mask):
            # input_ids: [Batch, Seq]
            # attention_mask: [Batch, Seq] (VITS2側から送られてくるので受け取る設定にする)

            x = self.emb(input_ids)  # [Batch, Seq, Dim]

            # Mean Pooling (Attention Mask を考慮して平均化)
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(x.size()).float()
            sum_embeddings = torch.sum(x * input_mask_expanded, 1)
            sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            pooled = sum_embeddings / sum_mask  # [B, 512]

            # 2. SSE 特有の変換とアップサイクル
            x_processed = self.dyt(pooled)
            x_processed = F.normalize(x_processed, p=2, dim=1)
            x_final = self.upcycle_proj(x_processed)  # [B, 1024]
            
            # 1. [B, 1024] -> [B, 1, 1024]
            x_unsqueezed = x_final.unsqueeze(1)

            # 2. 目標のシーケンス長を取得
            #target_seq_len = input_ids.size(1) + 2

            # 3. パディングする長さを計算 (Seq - 1)
            # ONNXで動的に扱うため、ここを 0 と比較して clamp しておくと安全です
            pad_len = 8192

            # 4. F.pad を使うのが最もスマートです
            # pad の引数は (最後の次元の前, 最後の次元の後, その前の次元の前, その前の次元の後...)
            # 今回は Seq次元 (dim 1) の後ろ側を pad_len 分だけ 0 で埋めたいので：
            # (Dim2の前, Dim2の後, Dim1の前, Dim1の後) -> (0, 0, 0, pad_len)
            res = F.pad(x_unsqueezed, (0, 0, 0, pad_len), "constant", 0)
    
            return res[0]


    wrapper = SSEForVITS2(sse_module).to("cpu")
    wrapper.eval()

    # ダミーデータ (Batch=1, Seq=10)
    dummy_input_ids = torch.zeros((1, 10), dtype=torch.long)
    dummy_mask = torch.ones((1, 10), dtype=torch.long)

    # エクスポート
    torch.onnx.export(
        wrapper,
        (dummy_input_ids, dummy_mask),
        onnx_temp_model_path,  # VITS2が読み込むパスに合わせて保存
        export_params=True,
        #opset_version=17,
        do_constant_folding=True,
        input_names=['input_ids', 'attention_mask'],  # VITS2側の名前と一致させる
        output_names=['output'],  # VITS2側が期待する名前に合わせる（通常これが多い）
        dynamic_axes={
            'input_ids': {0: 'batch_size', 1: 'sequence_length'},
            'attention_mask': {0: 'batch_size', 1: 'sequence_length'},
            #'last_hidden_state': {0: 'sequence_length'}
        }
    )

    onnx_model = onnx.load(onnx_temp_model_path)
    simplified_onnx_model, check = simplify(onnx_model)
    onnx.save(simplified_onnx_model, onnx_temp_model_path)
    
    #shape_inference.quant_pre_process(onnx_temp_model_path, onnx_temp_model_path)

    quantized_model = quantize_dynamic(onnx_temp_model_path, onnx_fp16_model_path, weight_type=QuantType.QInt8)

if __name__ == '__main__':
    export()
