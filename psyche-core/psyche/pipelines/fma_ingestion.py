"""
FMA Data Ingestion Pipeline — Week 1 Days 3-5.

Downloads, validates, and organizes the FMA-small dataset.
Quality gates: validate all audio files, quarantine corrupt ones.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class FMAIngestionPipeline:
    """Ingest and validate FMA-small dataset."""

    def __init__(
        self,
        raw_dir: str = "data/raw/fma_small",
        validated_dir: str = "data/validated",
        quarantine_dir: str = "data/quarantine",
        max_workers: int = 4,
    ):
        self.raw_dir = Path(raw_dir)
        self.validated_dir = Path(validated_dir)
        self.quarantine_dir = Path(quarantine_dir)
        self.max_workers = max_workers

    def validate_dataset(self) -> Dict[str, int]:
        """
        Validate all audio files in the FMA-small dataset.
        Returns: {total, valid, corrupt, validation_rate}
        """
        import librosa
        import soundfile as sf

        audio_files = list(self.raw_dir.rglob("*.mp3"))
        total = len(audio_files)
        valid = 0
        corrupt = 0
        tracks: List[Dict] = []

        self.validated_dir.mkdir(parents=True, exist_ok=True)
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)

        for audio_path in audio_files:
            try:
                y, sr = librosa.load(str(audio_path), sr=22050, duration=30)
                if len(y) < sr * 1:  # Less than 1 second = invalid
                    raise ValueError(f"Audio too short: {len(y)} samples")

                track_id = audio_path.stem
                tracks.append({
                    "track_id": track_id,
                    "path": str(audio_path),
                    "duration_samples": len(y),
                    "sample_rate": sr,
                })
                valid += 1

            except Exception as e:
                corrupt += 1
                logger.warning(f"Corrupt file {audio_path}: {e}")
                # Log quarantine reason
                quarantine_log = self.quarantine_dir / f"{audio_path.stem}.json"
                quarantine_log.write_text(json.dumps({
                    "file": str(audio_path),
                    "error": str(e),
                }))

        # Write manifest
        manifest = {
            "dataset": "fma-small",
            "total": total,
            "valid": valid,
            "corrupt": corrupt,
            "validation_rate": valid / max(total, 1),
            "tracks": tracks,
        }
        manifest_path = self.validated_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))

        logger.info(
            f"FMA validation: {valid}/{total} valid ({corrupt} corrupt, "
            f"{manifest['validation_rate']:.1%} rate)"
        )

        return manifest

    def extract_metadata(self, tracks_csv: str = "data/raw/fma_metadata/tracks.csv") -> Dict:
        """Extract and merge FMA track metadata."""
        import pandas as pd

        tracks_path = Path(tracks_csv)
        if not tracks_path.exists():
            logger.warning(f"Metadata CSV not found: {tracks_csv}")
            return {}

        df = pd.read_csv(str(tracks_path), header=[0, 1], index_col=0)
        metadata = {}

        for track_id in df.index:
            try:
                metadata[str(track_id)] = {
                    "title": str(df.loc[track_id, ("track", "title")]),
                    "artist": str(df.loc[track_id, ("artist", "name")]),
                    "genre": str(df.loc[track_id, ("track", "genre_top")]),
                    "duration": float(df.loc[track_id, ("track", "duration")]),
                }
            except (KeyError, ValueError):
                continue

        metadata_path = self.validated_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2))

        return metadata
