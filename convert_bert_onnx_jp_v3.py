import torch
import torch.nn as nn
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

import onnx
from onnxsim import simplify
from onnxruntime.quantization import quantize_dynamic, QuantType

def export():

    onnx_temp_model_path = "./bert/sse-fast-ja-onnx/model.onnx"
    onnx_fp16_model_path = "./bert/sse-fast-ja-onnx/model_fp16.onnx"

    # 1. モデルのロード
    model_id = "RikkaBotan/stable-static-embedding-fast-retrieval-mrl-ja"
    st_model = SentenceTransformer(model_id, trust_remote_code=True)
    sse_module = st_model[0]

    class SSEForVITS2(nn.Module):
        def __init__(self, sse):
            super().__init__()
            # EmbeddingBag ではなく、2次元入力に対応した通常の Embedding に差し替え
            self.emb = nn.Embedding.from_pretrained(sse.embedding.weight)
            self.dyt = sse.dyt

        def forward(self, input_ids, attention_mask):
            # input_ids: [Batch, Seq]
            # attention_mask: [Batch, Seq] (VITS2側から送られてくるので受け取る設定にする)

            x = self.emb(input_ids)  # [Batch, Seq, Dim]

            # Mean Pooling (Attention Mask を考慮して平均化)
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(x.size()).float()
            sum_embeddings = torch.sum(x * input_mask_expanded, 1)
            sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            x = sum_embeddings / sum_mask

            # DyT 処理 (SSE 独自の層)
            x = self.dyt(x)

            # L2 Normalize
            return F.normalize(x, p=2, dim=1)

    wrapper = SSEForVITS2(sse_module).to("cpu").half()
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
        output_names=['last_hidden_state'],  # VITS2側が期待する名前に合わせる（通常これが多い）
        dynamic_axes={
            'input_ids': {0: 'batch_size', 1: 'sequence_length'},
            'attention_mask': {0: 'batch_size', 1: 'sequence_length'},
            'last_hidden_state': {0: 'batch_size'}
        }
    )

    onnx_model = onnx.load(onnx_temp_model_path)
    simplified_onnx_model, check = simplify(onnx_model)
    onnx.save(simplified_onnx_model, onnx_fp16_model_path)

if __name__ == '__main__':
    export()