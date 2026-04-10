"""
MERT & CLAP Embedding Pipeline — Deep audio representations.

MERT: Music Understanding Model (768-dim embeddings)
      - Pre-trained on large-scale music data
      - Captures musical structure, harmony, rhythm

CLAP: Contrastive Language-Audio Pretraining (512-dim embeddings)
      - Text-audio aligned embeddings
      - Enables text-based music retrieval ("relaxing piano music")

Both require HuggingFace model access. Will run on GPU if available.
"""

import logging
from pathlib import Path
from typing import List, Optional

import numpy as np

logger = logging.getLogger(__name__)


class MERTEmbeddingPipeline:
    """Generate MERT embeddings for audio tracks."""

    def __init__(
        self,
        model_name: str = "m-a-p/MERT-v1-95M",
        device: str = "auto",
    ):
        self.model_name = model_name
        self.device = device
        self._model = None
        self._processor = None

    def _load_model(self):
        """Lazy-load MERT model."""
        if self._model is not None:
            return

        try:
            import torch
            from transformers import AutoModel, AutoFeatureExtractor

            self._processor = AutoFeatureExtractor.from_pretrained(
                self.model_name, trust_remote_code=True
            )
            self._model = AutoModel.from_pretrained(
                self.model_name, trust_remote_code=True
            )

            if self.device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self._model = self._model.to(self.device)
            self._model.eval()

            logger.info(f"MERT model loaded on {self.device}")
        except ImportError:
            logger.error(
                "transformers/torch not installed. "
                "Run: pip install torch transformers"
            )
            raise

    def embed_audio(self, audio: np.ndarray, sr: int = 22050) -> np.ndarray:
        """Generate MERT embedding for a single audio array."""
        import torch

        self._load_model()

        inputs = self._processor(
            audio, sampling_rate=sr, return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self._model(**inputs)
            # Pool over time: mean of last hidden state
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze()
            return embedding.cpu().numpy()

    def batch_embed(
        self,
        audio_paths: List[str],
        sr: int = 22050,
        duration: float = 30.0,
    ) -> np.ndarray:
        """Batch-embed audio files. Returns (n, 768) array."""
        from psyche.utils.audio import load_audio

        embeddings = []
        for i, path in enumerate(audio_paths):
            try:
                audio, sr_out = load_audio(path, sr=sr, duration=duration)
                emb = self.embed_audio(audio, sr_out)
                embeddings.append(emb)

                if (i + 1) % 50 == 0:
                    logger.info(f"MERT: embedded {i + 1}/{len(audio_paths)}")
            except Exception as e:
                logger.warning(f"MERT failed for {path}: {e}")
                embeddings.append(np.zeros(768, dtype=np.float32))

        return np.array(embeddings, dtype=np.float32)


class CLAPEmbeddingPipeline:
    """Generate CLAP embeddings for audio tracks."""

    def __init__(
        self,
        model_name: str = "laion/larger_clap_music",
        device: str = "auto",
    ):
        self.model_name = model_name
        self.device = device
        self._model = None
        self._processor = None

    def _load_model(self):
        """Lazy-load CLAP model."""
        if self._model is not None:
            return

        try:
            import torch
            from transformers import ClapModel, ClapProcessor

            self._processor = ClapProcessor.from_pretrained(self.model_name)
            self._model = ClapModel.from_pretrained(self.model_name)

            if self.device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self._model = self._model.to(self.device)
            self._model.eval()

            logger.info(f"CLAP model loaded on {self.device}")
        except ImportError:
            logger.error(
                "transformers/torch not installed. "
                "Run: pip install torch transformers"
            )
            raise

    def embed_audio(self, audio: np.ndarray, sr: int = 48000) -> np.ndarray:
        """Generate CLAP audio embedding."""
        import torch

        self._load_model()

        inputs = self._processor(
            audios=[audio], sampling_rate=sr, return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self._model.get_audio_features(**inputs)
            return outputs.squeeze().cpu().numpy()

    def embed_text(self, text: str) -> np.ndarray:
        """Generate CLAP text embedding (for text-to-music retrieval)."""
        import torch

        self._load_model()

        inputs = self._processor(text=[text], return_tensors="pt", padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self._model.get_text_features(**inputs)
            return outputs.squeeze().cpu().numpy()

    def batch_embed(
        self,
        audio_paths: List[str],
        sr: int = 48000,
        duration: float = 30.0,
    ) -> np.ndarray:
        """Batch-embed audio files. Returns (n, 512) array."""
        from psyche.utils.audio import load_audio

        embeddings = []
        for i, path in enumerate(audio_paths):
            try:
                audio, sr_out = load_audio(path, sr=sr, duration=duration)
                emb = self.embed_audio(audio, sr_out)
                embeddings.append(emb)

                if (i + 1) % 50 == 0:
                    logger.info(f"CLAP: embedded {i + 1}/{len(audio_paths)}")
            except Exception as e:
                logger.warning(f"CLAP failed for {path}: {e}")
                embeddings.append(np.zeros(512, dtype=np.float32))

        return np.array(embeddings, dtype=np.float32)
