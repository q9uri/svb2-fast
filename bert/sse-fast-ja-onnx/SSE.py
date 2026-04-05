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


class SSE(InputModule):
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
    
    def save(
        self,
        output_path: str,
        *args,
        safe_serialization: bool = True,
        **kwargs,
    ) -> None:
        os.makedirs(output_path, exist_ok=True)

        if safe_serialization:
            save_safetensors_file(
                self.state_dict(),
                os.path.join(output_path, "model.safetensors"),
            )
        else:
            torch.save(
                self.state_dict(),
                os.path.join(output_path, "pytorch_model.bin"),
            )

        self.tokenizer.save(
            str(Path(output_path) / "tokenizer.json")
        )

    @classmethod
    def load(
        cls,
        model_name_or_path: str,
        **kwargs,
    ):
        allowed_keys = {
            "cache_dir",
            "local_files_only",
            "force_download",
        }
        filtered_kwargs = {
            k: v for k, v in kwargs.items() if k in allowed_keys
        }
    
        tokenizer_path = cls.load_file_path(
            model_name_or_path,
            filename="tokenizer.json",
            **filtered_kwargs,
        )
        tokenizer = Tokenizer.from_file(tokenizer_path)
    
        weights = cls.load_torch_weights(
            model_name_or_path=model_name_or_path,
            **filtered_kwargs,
        )
    
        hidden_dim = weights["embedding.weight"].size(1)
        vocab_size = weights["embedding.weight"].size(0)
    
        model = cls(
            tokenizer=tokenizer,
            vocab_size=vocab_size,
            hidden_dim=hidden_dim,
        )
    
        model.load_state_dict(weights)
        return model


@dataclass
class SSESforzandoConfig:
    hidden_dim: int = 512
    vocab_size: int = 30522


@dataclass
class SSEForzandoConfig:
    hidden_dim: int = 384
    vocab_size: int = 30522

@dataclass
class SSESforzandoBiConfig:
    hidden_dim: int = 512
    vocab_size: int = 96867

@dataclass
class SSEForzandoBiConfig:
    hidden_dim: int = 384
    vocab_size: int = 96867

@dataclass
class SSESforzandoJConfig:
    hidden_dim: int = 512
    vocab_size: int = 32768

@dataclass
class SSEForzandoJConfig:
    hidden_dim: int = 384
    vocab_size: int = 32768
