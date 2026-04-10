"""
FMA Dataset Downloader — Windows-compatible.

Downloads FMA-small (~7.2GB) audio + metadata from the official source.
Supports resume on interruption.

Usage:
    python scripts/download_fma.py
    python scripts/download_fma.py --dataset small   (default)
    python scripts/download_fma.py --dataset medium   (25GB, 25k tracks)
"""

import argparse
import os
import shutil
import sys
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm

# FMA download URLs
FMA_URLS = {
    "small": "https://os.unil.cloud.switch.ch/fma/fma_small.zip",
    "medium": "https://os.unil.cloud.switch.ch/fma/fma_medium.zip",
    "metadata": "https://os.unil.cloud.switch.ch/fma/fma_metadata.zip",
}


def download_file(url: str, dest: Path, chunk_size: int = 8192) -> None:
    """Download a file with progress bar, supporting resume."""
    headers = {}
    initial_size = 0

    if dest.exists():
        initial_size = dest.stat().st_size
        headers["Range"] = f"bytes={initial_size}-"

    response = requests.get(url, headers=headers, stream=True, timeout=30)

    if response.status_code == 416:
        print(f"  ✓ Already downloaded: {dest.name}")
        return

    total_size = int(response.headers.get("content-length", 0)) + initial_size
    mode = "ab" if initial_size > 0 else "wb"

    if initial_size > 0:
        print(f"  Resuming from {initial_size / 1e9:.1f} GB...")

    with open(dest, mode) as f, tqdm(
        total=total_size,
        initial=initial_size,
        unit="B",
        unit_scale=True,
        desc=dest.name,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))


def extract_zip(zip_path: Path, dest_dir: Path) -> None:
    """Extract a zip file with progress."""
    print(f"  Extracting {zip_path.name}...")
    with zipfile.ZipFile(str(zip_path), "r") as zf:
        members = zf.namelist()
        for member in tqdm(members, desc="Extracting", unit="file"):
            zf.extract(member, str(dest_dir))
    print(f"  ✓ Extracted to {dest_dir}")


def main():
    parser = argparse.ArgumentParser(description="Download FMA dataset")
    parser.add_argument(
        "--dataset",
        choices=["small", "medium"],
        default="small",
        help="Dataset size (default: small, ~7.2GB)",
    )
    parser.add_argument(
        "--data-dir",
        default="data/raw",
        help="Directory to save data (default: data/raw)",
    )
    parser.add_argument(
        "--skip-metadata",
        action="store_true",
        help="Skip metadata download",
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    zip_dir = data_dir / "downloads"
    zip_dir.mkdir(exist_ok=True)

    dataset_key = args.dataset
    audio_dir = data_dir / f"fma_{dataset_key}"

    print(f"=== FMA Dataset Download (fma_{dataset_key}) ===")
    print(f"Target: {data_dir.resolve()}")
    print()

    # Download audio
    if audio_dir.exists() and any(audio_dir.rglob("*.mp3")):
        mp3_count = len(list(audio_dir.rglob("*.mp3")))
        print(f"✓ Audio already exists: {mp3_count} mp3 files in {audio_dir}")
    else:
        audio_zip = zip_dir / f"fma_{dataset_key}.zip"
        print(f"Downloading fma_{dataset_key}.zip...")
        download_file(FMA_URLS[dataset_key], audio_zip)
        extract_zip(audio_zip, data_dir)
        print(f"✓ Audio extracted to {audio_dir}")

    # Download metadata
    metadata_dir = data_dir / "fma_metadata"
    if not args.skip_metadata:
        if metadata_dir.exists() and any(metadata_dir.glob("*.csv")):
            print(f"✓ Metadata already exists in {metadata_dir}")
        else:
            meta_zip = zip_dir / "fma_metadata.zip"
            print(f"Downloading fma_metadata.zip...")
            download_file(FMA_URLS["metadata"], meta_zip)
            extract_zip(meta_zip, data_dir)
            print(f"✓ Metadata extracted to {metadata_dir}")

    # Summary
    print()
    print("=== Download Complete ===")
    if audio_dir.exists():
        mp3_count = len(list(audio_dir.rglob("*.mp3")))
        print(f"  Audio: {mp3_count} mp3 files")
    if metadata_dir.exists():
        csv_count = len(list(metadata_dir.glob("*.csv")))
        print(f"  Metadata: {csv_count} csv files")
    print()
    print("Next steps:")
    print("  1. Run validation: python scripts/run_pipeline.py --step validate")
    print("  2. Extract features: python scripts/run_pipeline.py --step features")
    print("  3. Build FAISS index: python scripts/run_pipeline.py --step index")


if __name__ == "__main__":
    main()
