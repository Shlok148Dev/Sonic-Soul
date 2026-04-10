#!/bin/bash
# Download FMA-small dataset (~7.2GB)
# Source: https://github.com/mdeff/fma

set -e

DATA_DIR="data/raw"
mkdir -p "$DATA_DIR"

echo "=== Downloading FMA-small (8,000 tracks, 30s clips) ==="
echo "This will download ~7.2GB of audio data."

# FMA-small audio
if [ ! -d "$DATA_DIR/fma_small" ]; then
    echo "Downloading fma_small.zip..."
    curl -L -o "$DATA_DIR/fma_small.zip" \
        "https://os.unil.cloud.switch.ch/fma/fma_small.zip"
    echo "Extracting..."
    unzip -q "$DATA_DIR/fma_small.zip" -d "$DATA_DIR/"
    rm "$DATA_DIR/fma_small.zip"
    echo "✓ FMA-small audio extracted to $DATA_DIR/fma_small/"
else
    echo "✓ FMA-small audio already exists"
fi

# FMA metadata
if [ ! -d "$DATA_DIR/fma_metadata" ]; then
    echo "Downloading fma_metadata.zip..."
    curl -L -o "$DATA_DIR/fma_metadata.zip" \
        "https://os.unil.cloud.switch.ch/fma/fma_metadata.zip"
    echo "Extracting..."
    unzip -q "$DATA_DIR/fma_metadata.zip" -d "$DATA_DIR/"
    rm "$DATA_DIR/fma_metadata.zip"
    echo "✓ FMA metadata extracted to $DATA_DIR/fma_metadata/"
else
    echo "✓ FMA metadata already exists"
fi

echo ""
echo "=== FMA Download Complete ==="
echo "Audio: $DATA_DIR/fma_small/ (~8000 tracks)"
echo "Metadata: $DATA_DIR/fma_metadata/"
echo ""
echo "Next: Run the validation pipeline"
echo "  python -m psyche.pipelines.fma_ingestion"
