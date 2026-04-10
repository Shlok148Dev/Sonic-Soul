"""
PSYCHE Audio Utilities — FFmpeg, librosa wrappers, validation.
"""

import logging
import subprocess
from pathlib import Path
from typing import Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)


def load_audio(
    path: str,
    sr: int = 22050,
    duration: Optional[float] = 30.0,
    mono: bool = True,
) -> Tuple[np.ndarray, int]:
    """
    Load audio file with fallback handling.
    Returns (audio_array, sample_rate).
    """
    import librosa

    try:
        y, sr_out = librosa.load(path, sr=sr, duration=duration, mono=mono)
        return y, sr_out
    except Exception as e:
        logger.warning(f"librosa failed for {path}: {e}. Trying soundfile...")
        import soundfile as sf
        data, sr_out = sf.read(path, dtype="float32")
        if mono and data.ndim > 1:
            data = np.mean(data, axis=1)
        if duration:
            max_samples = int(sr_out * duration)
            data = data[:max_samples]
        return data, sr_out


def validate_audio_file(path: str, min_duration_s: float = 1.0) -> bool:
    """Check if an audio file is valid and above minimum duration."""
    try:
        y, sr = load_audio(path, duration=None)
        duration = len(y) / sr
        if duration < min_duration_s:
            return False
        return True
    except Exception:
        return False


def convert_to_wav(
    input_path: str,
    output_path: str,
    sr: int = 22050,
    channels: int = 1,
) -> bool:
    """Convert audio file to WAV using FFmpeg."""
    try:
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-ar", str(sr), "-ac", str(channels),
            output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"FFmpeg conversion failed: {e}")
        return False
