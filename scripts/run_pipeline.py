"""
PSYCHE Data Pipeline Runner — Master script for all pipeline stages.

Usage:
    python scripts/run_pipeline.py --step validate
    python scripts/run_pipeline.py --step features
    python scripts/run_pipeline.py --step index
    python scripts/run_pipeline.py --step baselines
    python scripts/run_pipeline.py --step all
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

# Add psyche-core to path
sys.path.insert(0, str(Path(__file__).parent.parent / "psyche-core"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("pipeline")


def step_validate():
    """Step 1: Validate FMA dataset — check all audio files load."""
    from psyche.pipelines.fma_ingestion import FMAIngestionPipeline

    logger.info("=== Step 1: Validating FMA dataset ===")
    pipeline = FMAIngestionPipeline()

    if not pipeline.raw_dir.exists():
        logger.error(
            f"FMA data not found at {pipeline.raw_dir}. "
            "Run: python scripts/download_fma.py"
        )
        return False

    manifest = pipeline.validate_dataset()
    logger.info(
        f"Validation complete: {manifest['valid']}/{manifest['total']} tracks valid "
        f"({manifest['corrupt']} corrupt, {manifest['validation_rate']:.1%} rate)"
    )

    if manifest["validation_rate"] < 0.99:
        logger.warning("Validation rate below 99% — check quarantine files")

    return True


def step_features():
    """Step 2: Extract librosa features from validated tracks."""
    from psyche.pipelines.feature_extraction import FeatureExtractionPipeline

    logger.info("=== Step 2: Extracting audio features (librosa) ===")
    manifest_path = Path("data/validated/manifest.json")

    if not manifest_path.exists():
        logger.error("No manifest found. Run --step validate first.")
        return False

    pipeline = FeatureExtractionPipeline()
    pipeline.batch_extract(str(manifest_path))

    output = Path("data/features/librosa_features.parquet")
    if output.exists():
        import pandas as pd
        df = pd.read_parquet(str(output))
        logger.info(f"Features extracted for {len(df)} tracks → {output}")
        return True
    else:
        logger.error("Feature extraction failed — no output file.")
        return False


def step_embeddings():
    """Step 2.5: Extract MERT and CLAP embeddings from validated tracks."""
    from psyche.pipelines.embeddings import MERTEmbeddingPipeline, CLAPEmbeddingPipeline
    
    logger.info("=== Step 2.5: Extracting Deep Embeddings (MERT + CLAP) ===")
    manifest_path = Path("data/validated/manifest.json")

    if not manifest_path.exists():
        logger.error("No manifest found. Run --step validate first.")
        return False

    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    
    audio_paths = [t["processed_path"] for t in manifest.get("tracks", []) if t["status"] == "valid"]
    if not audio_paths:
        logger.error("No valid tracks found to embed.")
        return False

    # Ensure output dir exists
    out_dir = Path("data/features")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Extract MERT
    output_mert = out_dir / "mert_embeddings.npy"
    if not output_mert.exists():
        logger.info(f"Extracting MERT embeddings for {len(audio_paths)} tracks...")
        mert_pipeline = MERTEmbeddingPipeline(device="cpu") # Force cpu for stability
        mert_embeddings = mert_pipeline.batch_embed(audio_paths)
        import numpy as np
        np.save(str(output_mert), mert_embeddings)
        logger.info(f"MERT embeddings saved to {output_mert}")
    else:
        logger.info("MERT embeddings already exist.")

    # Extract CLAP
    output_clap = out_dir / "clap_embeddings.npy"
    if not output_clap.exists():
        logger.info(f"Extracting CLAP embeddings for {len(audio_paths)} tracks...")
        clap_pipeline = CLAPEmbeddingPipeline(device="cpu")
        clap_embeddings = clap_pipeline.batch_embed(audio_paths)
        import numpy as np
        np.save(str(output_clap), clap_embeddings)
        logger.info(f"CLAP embeddings saved to {output_clap}")
    else:
        logger.info("CLAP embeddings already exist.")

    return True


def step_index():
    """Step 3: Build FAISS indexes from extracted features."""
    from psyche.pipelines.embedding_index import EmbeddingIndexBuilder
    import json

    logger.info("=== Step 3: Building FAISS indexes ===")

    manifest_path = Path("data/validated/manifest.json")
    if not manifest_path.exists():
        logger.error("No manifest found. Run --step validate first.")
        return False
        
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    track_ids = [t["id"] for t in manifest.get("tracks", []) if t["status"] == "valid"]

    import numpy as np
    
    output_mert = Path("data/features/mert_embeddings.npy")
    output_clap = Path("data/features/clap_embeddings.npy")
    
    builder = EmbeddingIndexBuilder()
    
    built_any = False
    if output_mert.exists():
        logger.info("Building MERT FAISS index...")
        mert_embeddings = np.load(str(output_mert))
        builder.build_index(mert_embeddings, track_ids, "mert_index")
        built_any = True
    else:
        logger.warning("MERT embeddings not found for indexing.")
        
    if output_clap.exists():
        logger.info("Building CLAP FAISS index...")
        clap_embeddings = np.load(str(output_clap))
        builder.build_index(clap_embeddings, track_ids, "clap_index")
        built_any = True
    else:
        logger.warning("CLAP embeddings not found for indexing.")

    if not built_any:
        # Fallback to MFCC-based index
        features_path = Path("data/features/librosa_features.parquet")
        if features_path.exists():
            import pandas as pd
            df = pd.read_parquet(str(features_path))
            logger.info("Building MFCC index (MERT proxy)...")
            mfcc_cols = [col for col in df.columns if col.startswith("mfcc_mean")]
            if not mfcc_cols:
                mfcc_embeddings = np.array(df["mfcc_mean"].tolist(), dtype=np.float32)
            else:
                mfcc_embeddings = df[mfcc_cols].values.astype(np.float32)
            mfcc_track_ids = df["track_id"].tolist()
            builder.build_index(mfcc_embeddings, mfcc_track_ids, "mert_index")
        else:
             logger.error("No features found to build index.")
             return False

    logger.info("FAISS indexes built successfully")
    return True



def step_baselines():
    """Step 4: Run baseline recommenders B0-B4."""
    logger.info("=== Step 4: Running baseline recommenders ===")

    features_path = Path("data/features/librosa_features.parquet")
    if not features_path.exists():
        logger.error("No features found. Run --step features first.")
        return False

    import numpy as np
    import pandas as pd

    df = pd.read_parquet(str(features_path))
    track_ids = df["track_id"].tolist()

    results = {}

    # B0: Random
    logger.info("B0: Random recommender...")
    random_recs = list(np.random.choice(track_ids, size=min(10, len(track_ids)), replace=False))
    from psyche.utils.metrics import serendipity_rate, gini_coefficient
    fake_history = set(track_ids[:100])
    results["B0_random"] = {
        "serendipity": serendipity_rate(random_recs, fake_history),
        "method": "random",
    }
    logger.info(f"  B0 serendipity: {results['B0_random']['serendipity']:.3f}")

    # B1: Popularity-weighted random (using energy as proxy for popularity)
    logger.info("B1: Popularity-weighted random...")
    energies = df.get("energy", pd.Series([0.5] * len(df)))
    probs = energies.values / energies.sum()
    pop_recs = list(np.random.choice(track_ids, size=10, replace=False, p=probs))
    results["B1_popularity"] = {
        "serendipity": serendipity_rate(pop_recs, fake_history),
        "method": "popularity_weighted",
    }
    logger.info(f"  B1 serendipity: {results['B1_popularity']['serendipity']:.3f}")

    # B2: MFCC cosine similarity
    logger.info("B2: MFCC cosine similarity...")
    mfcc_data = np.array(df["mfcc_mean"].tolist(), dtype=np.float32)
    if len(mfcc_data) > 0:
        from sklearn.metrics.pairwise import cosine_similarity
        query = mfcc_data[0:1]
        sims = cosine_similarity(query, mfcc_data)[0]
        top_k = np.argsort(sims)[-11:-1][::-1]  # top 10, exclude self
        mfcc_recs = [track_ids[i] for i in top_k]
        results["B2_mfcc_sim"] = {
            "serendipity": serendipity_rate(mfcc_recs, fake_history),
            "method": "mfcc_cosine",
        }
        logger.info(f"  B2 serendipity: {results['B2_mfcc_sim']['serendipity']:.3f}")

    # Save results
    output = Path("data/evaluation")
    output.mkdir(parents=True, exist_ok=True)
    results_path = output / "baseline_results.json"
    results_path.write_text(json.dumps(results, indent=2))
    logger.info(f"Baseline results saved to {results_path}")

    return True


def main():
    parser = argparse.ArgumentParser(description="PSYCHE Data Pipeline Runner")
    parser.add_argument(
        "--step",
        choices=["validate", "features", "embeddings", "index", "baselines", "all"],
        required=True,
        help="Pipeline step to run",
    )
    args = parser.parse_args()

    steps = {
        "validate": step_validate,
        "features": step_features,
        "embeddings": step_embeddings,
        "index": step_index,
        "baselines": step_baselines,
    }

    if args.step == "all":
        for name, func in steps.items():
            logger.info(f"\n{'='*60}")
            start = time.time()
            success = func()
            elapsed = time.time() - start
            status = "✓" if success else "✗"
            logger.info(f"{status} {name} completed in {elapsed:.1f}s")
            if not success:
                logger.error(f"Pipeline failed at step: {name}")
                sys.exit(1)
    else:
        start = time.time()
        success = steps[args.step]()
        elapsed = time.time() - start
        status = "✓" if success else "✗"
        logger.info(f"{status} {args.step} completed in {elapsed:.1f}s")
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
