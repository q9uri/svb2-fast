"""
coding = utf-8
Copyright 2026 Rikka Botan. All rights reserved
Licensed under "MIT License"
Stable Static Embedding official PyTorch implementation
"""

from __future__ import annotations
import os
from pathlib import Path
from safetensors.torch import save_file as save_safetensors_file
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict
from dataclasses import dataclass
from tokenizers import Tokenizer
from transformers import PreTrainedTokenizerFast
from sentence_transformers.models.InputModule import InputModule
from safetensors.torch import load_file


def quantize_q4_k_m(weight: torch.Tensor):
    """
    weight: (vocab, dim)
    returns: packed uint8 + scale + zero
    """
    w = weight.detach().cpu().numpy().astype(np.float32)

    scales = np.max(np.abs(w), axis=1, keepdims=True) + 1e-8
    w_norm = w / scales

    q = np.clip(np.round((w_norm + 1) * 7.5), 0, 15).astype(np.uint8)

    # pack 2x4bit -> uint8
    packed = (q[:, 0::2] << 4) | q[:, 1::2]

    return {
        "packed": packed,
        "scales": scales.astype(np.float32),
    }


def dequantize_q4_k_m(packed: np.ndarray, scales: np.ndarray):
    hi = (packed >> 4) & 0xF
    lo = packed & 0xF

    q = np.empty((packed.shape[0], packed.shape[1]*2), dtype=np.uint8)
    q[:, 0::2] = hi
    q[:, 1::2] = lo

    w = (q.astype(np.float32) / 7.5) - 1.0
    w = w * scales
    return torch.from_numpy(w)


class SeparableDyT(nn.Module):
    def __init__(
        self,
        hidden_dim: int,
        alpha_init: float = 0.5
    ):
        super().__init__()
        self.alpha = nn.Parameter(alpha_init*torch.ones(hidden_dim))
        self.beta = nn.Parameter(torch.ones(hidden_dim))
        self.bias = nn.Parameter(torch.zeros(hidden_dim))
    
    def forward(
        self,
        x: torch.Tensor
    ) -> torch.Tensor:
        x = self.beta * F.tanh(self.alpha * x + self.bias)
        return x


class SSEQ(InputModule):
    """
    Stable Static Embedding (SSE)
    StaticEmbedding-compatible Sentence-Transformers module
    """

    def __init__(
        self,
        tokenizer: Tokenizer | PreTrainedTokenizerFast,
        vocab_size: int,
        hidden_dim: int = 1024,
        **kwargs,
    ):
        super().__init__()

        if isinstance(tokenizer, PreTrainedTokenizerFast):
            tokenizer = tokenizer._tokenizer
        elif not isinstance(tokenizer, Tokenizer):
            raise ValueError("Tokenizer must be a fast (Rust) tokenizer")

        self.tokenizer: Tokenizer = tokenizer
        self.tokenizer.no_padding()

        self.embedding = nn.EmbeddingBag(vocab_size, hidden_dim)
        self.dyt = SeparableDyT(hidden_dim)

        self.embedding_dim = hidden_dim

        # For model card compatibility
        self.base_model = kwargs.get("base_model", None)

    # Tokenization (StaticEmbedding-compatible)
    def tokenize(
        self,
        texts: list[str],
        **kwargs
    ) -> dict[str, torch.Tensor]:
        encodings = self.tokenizer.encode_batch(texts, add_special_tokens=False)
        encodings_ids = [encoding.ids for encoding in encodings]

        offsets = torch.from_numpy(
            np.cumsum(
                [0] + [len(token_ids) for token_ids in encodings_ids[:-1]]
            )
        )
        input_ids = torch.tensor(
            [token_id for token_ids in encodings_ids for token_id in token_ids],
            dtype=torch.long
        )
        return {
            "input_ids": input_ids,
            "offsets": offsets
        }

    # Forward
    def forward(
        self,
        features: Dict[str, torch.Tensor],
        **kwargs,
    ) -> Dict[str, torch.Tensor]:
        x = self.embedding(features["input_ids"], features["offsets"])
        x = self.dyt(x)
        features["sentence_embedding"] = x
        return features

    # Required APIs
    def get_sentence_embedding_dimension(self) -> int:
        return self.embedding_dim

    @property
    def max_seq_length(self) -> int:
        return torch.inf
    
    def save(self, output_path: str):
        os.makedirs(output_path, exist_ok=True)

        state = self.state_dict()

        emb = state["embedding.weight"]
        q = quantize_q4_k_m(emb)

        del state["embedding.weight"]

        save_safetensors_file(
            state,
            os.path.join(output_path, "model_rest.safetensors"),
        )

        with open(os.path.join(output_path, "embedding.q4_k_m.bin"), "wb") as f:
            f.write(q["packed"].tobytes())
            f.write(q["scales"].tobytes())

        self.tokenizer.save(
            str(Path(output_path) / "tokenizer.json")
        )
    
    @classmethod
    def load(cls, model_path: str):

        tokenizer = Tokenizer.from_file(
            os.path.join(model_path, "tokenizer.json")
        )

        state = load_file(
            os.path.join(model_path, "model_rest.safetensors"),
            device="cpu"
        )

        # read q4 binary
        bin_path = os.path.join(model_path, "embedding.q4_k_m.bin")
        with open(bin_path, "rb") as f:
            raw = f.read()

        hidden = state["dyt.alpha"].shape[0]
        total_uint8 = len(raw)

        bytes_per_row = hidden // 2 + 4
        vocab = total_uint8 // bytes_per_row

        packed_size = vocab * hidden // 2

        packed = np.frombuffer(raw[:packed_size], dtype=np.uint8)
        scales = np.frombuffer(raw[packed_size:], dtype=np.float32)

        packed = packed.reshape(vocab, hidden // 2)
        scales = scales.reshape(vocab, 1)

        emb = dequantize_q4_k_m(packed, scales)

        # rebuild model
        model = cls(
            tokenizer=tokenizer,
            vocab_size=emb.shape[0],
            hidden_dim=emb.shape[1]
        )

        state["embedding.weight"] = emb
        model.load_state_dict(state)

        return model


@dataclass
class SSESforzandoConfig:
    hidden_dim: int = 512
    vocab_size: int = 30522


@dataclass
class SSEForzandoConfig:
    hidden_dim: int = 384
    vocab_size: int = 30522
