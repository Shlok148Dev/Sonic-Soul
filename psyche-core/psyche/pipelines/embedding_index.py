"""
FAISS Embedding Index Builder.

Builds FAISS indexes for MERT (768-dim) and CLAP (512-dim) embeddings.
Used by Serendipity Agent and Coherence Architect for fast retrieval.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingIndexBuilder:
    """Build and manage FAISS vector indexes."""

    def __init__(self, features_dir: str = "data/features"):
        self.features_dir = Path(features_dir)
        self.features_dir.mkdir(parents=True, exist_ok=True)

    def build_index(
        self,
        embeddings: np.ndarray,
        track_ids: List[str],
        index_name: str,
    ) -> None:
        """
        Build a FAISS index from embeddings.
        Saves: {index_name}.faiss and {index_name}_id_map.json
        """
        import faiss

        dim = embeddings.shape[1]
        n = embeddings.shape[0]

        # Use IVF for large datasets, flat for small
        if n > 10000:
            nlist = min(int(np.sqrt(n)), 256)
            quantizer = faiss.IndexFlatL2(dim)
            index = faiss.IndexIVFFlat(quantizer, dim, nlist)
            index.train(embeddings.astype(np.float32))
        else:
            index = faiss.IndexFlatL2(dim)

        index.add(embeddings.astype(np.float32))

        index_path = self.features_dir / f"{index_name}.faiss"
        id_map_path = self.features_dir / f"{index_name}_id_map.json"

        faiss.write_index(index, str(index_path))

        id_map = {str(i): tid for i, tid in enumerate(track_ids)}
        id_map_path.write_text(json.dumps(id_map))

        logger.info(f"Built FAISS index '{index_name}': {n} vectors of dim {dim}")

    def search(
        self,
        query: np.ndarray,
        index_name: str,
        k: int = 10,
    ) -> List[Dict]:
        """Search a FAISS index and return track IDs with distances."""
        import faiss

        index_path = self.features_dir / f"{index_name}.faiss"
        id_map_path = self.features_dir / f"{index_name}_id_map.json"

        index = faiss.read_index(str(index_path))
        id_map = json.loads(id_map_path.read_text())

        distances, indices = index.search(query.astype(np.float32).reshape(1, -1), k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx >= 0:
                results.append({
                    "track_id": id_map[str(idx)],
                    "distance": float(dist),
                    "similarity": 1.0 / (1.0 + float(dist)),
                })

        return results
