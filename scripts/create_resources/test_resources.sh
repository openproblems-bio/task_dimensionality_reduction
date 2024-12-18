#!/bin/bash

# get the root of the directory
REPO_ROOT=$(git rev-parse --show-toplevel)

# ensure that the command below is run from the root of the repository
cd "$REPO_ROOT"

set -e

RAW_DATA=resources_test/common
DATASET_DIR=resources_test/task_dimensionality_reduction

mkdir -p $DATASET_DIR

# Process dataset
viash run src/data_processors/process_dataset/config.vsh.yaml -- \
    --input $RAW_DATA/cxg_mouse_pancreas_atlas/dataset.h5ad \
    --output_dataset $DATASET_DIR/cxg_mouse_pancreas_atlas/dataset.h5ad \
    --output_solution $DATASET_DIR/cxg_mouse_pancreas_atlas/solution.h5ad

# Run one method
viash run src/methods/pca/config.vsh.yaml -- \
    --input $DATASET_DIR/cxg_mouse_pancreas_atlas/dataset.h5ad \
    --output $DATASET_DIR/cxg_mouse_pancreas_atlas/embedding.h5ad

# Process embedding
viash run src/data_processors/process_embedding/config.vsh.yaml -- \
    --input_embedding $DATASET_DIR/cxg_mouse_pancreas_atlas/embedding.h5ad \
    --input_solution $DATASET_DIR/cxg_mouse_pancreas_atlas/solution.h5ad \
    --output $DATASET_DIR/cxg_mouse_pancreas_atlas/processed_embedding.h5ad

# Run one metric
viash run src/metrics/clustering_performance/config.vsh.yaml -- \
    --input_embedding $DATASET_DIR/cxg_mouse_pancreas_atlas/processed_embedding.h5ad \
    --input_solution $DATASET_DIR/cxg_mouse_pancreas_atlas/solution.h5ad \
    --output $DATASET_DIR/cxg_mouse_pancreas_atlas/score.h5ad

cat > $DATASET_DIR/cxg_mouse_pancreas_atlas/state.yaml << HERE
id: cxg_mouse_pancreas_atlas
output_dataset: !file dataset.h5ad
output_solution: !file solution.h5ad
HERE

# only run this if you have access to the openproblems-data bucket
aws s3 sync --profile op \
    "resources_test/task_dimensionality_reduction" \
    s3://openproblems-data/resources_test/task_dimensionality_reduction \
    --delete --dryrun
