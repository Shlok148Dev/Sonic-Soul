"""
Feature Extraction Pipeline — librosa + MERT + CLAP embeddings.

Extracts audio features in three tiers:
1. Basic: librosa MFCCs, spectral centroid, tempo, etc.
2. MERT: 768-dim music understanding embeddings
3. CLAP: 512-dim text-audio contrastive embeddings
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)


class FeatureExtractionPipeline:
    """Extract audio features at multiple representation levels."""

    def __init__(
        self,
        raw_dir: str = "data/raw/fma_small",
        features_dir: str = "data/features",
        sample_rate: int = 22050,
        max_workers: int = 4,
    ):
        self.raw_dir = Path(raw_dir)
        self.features_dir = Path(features_dir)
        self.sample_rate = sample_rate
        self.max_workers = max_workers
        self.features_dir.mkdir(parents=True, exist_ok=True)

    def extract_librosa_features(self, audio_path: str) -> Dict[str, Any]:
        """Extract basic audio features using librosa."""
        import librosa

        y, sr = librosa.load(audio_path, sr=self.sample_rate, duration=30)

        # MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfcc_mean = np.mean(mfccs, axis=1).tolist()

        # Spectral features
        spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        spectral_rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))
        spectral_bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))

        # Rhythm
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo_val = float(tempo) if np.isscalar(tempo) else float(tempo[0])

        # Chroma
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1).tolist()

        # Energy
        rms = librosa.feature.rms(y=y)
        energy = float(np.mean(rms))

        return {
            "mfcc_mean": mfcc_mean,
            "spectral_centroid": spectral_centroid,
            "spectral_rolloff": spectral_rolloff,
            "spectral_bandwidth": spectral_bandwidth,
            "tempo": tempo_val,
            "chroma_mean": chroma_mean,
            "energy": energy,
        }

    def batch_extract(self, manifest_path: str = "data/validated/manifest.json") -> None:
        """
        Batch extract features for all validated tracks.
        Saves to data/features/librosa_features.parquet
        """
        import pandas as pd

        manifest = json.loads(Path(manifest_path).read_text())
        tracks = manifest["tracks"]

        results = []
        for i, track in enumerate(tracks):
            try:
                features = self.extract_librosa_features(track["path"])
                features["track_id"] = track["track_id"]
                results.append(features)

                if (i + 1) % 100 == 0:
                    logger.info(f"Extracted features for {i + 1}/{len(tracks)} tracks")

            except Exception as e:
                logger.warning(f"Feature extraction failed for {track['track_id']}: {e}")

        df = pd.DataFrame(results)
        output_path = self.features_dir / "librosa_features.parquet"
        df.to_parquet(str(output_path))
        logger.info(f"Saved {len(results)} feature vectors to {output_path}")
