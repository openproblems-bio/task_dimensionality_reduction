#!/bin/bash

# get the root of the directory
REPO_ROOT=$(git rev-parse --show-toplevel)

# ensure that the command below is run from the root of the repository
cd "$REPO_ROOT"

# # remove this when you have implemented the script
# echo "TODO: once the 'run_benchmark' workflow has been implemented, update this script to use it."
# echo "  Step 1: replace 'task_template' with the name of the task in the following command."
# echo "  Step 2: replace the rename keys parameters to fit your run_benchmark inputs"
# echo "  Step 3: replace the settings parameter to fit your run_benchmark outputs"
# echo "  Step 4: remove this message"
# exit 1

set -e

# write the parameters to file
cat > /tmp/params.yaml << 'HERE'
input_dataset: s3://openproblems-data/resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/dataset.h5ad
input_solution: s3://openproblems-data/resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/solution.h5ad
output_state: "state.yaml"
publish_dir: s3://openproblems-nextflow/temp/task_dimensionality_reduction/
HERE

tw launch https://github.com/openproblems-bio/task_dimensionality_reduction.git \
  --revision build/main \
  --pull-latest \
  --main-script target/nextflow/workflows/run_benchmark/main.nf \
  --workspace 53907369739130 \
  --compute-env 5DwwhQoBi0knMSGcwThnlF \
  --params-file /tmp/params.yaml \
  --config common/nextflow_helpers/labels_tw.config \
  --labels task_dimensionality_reduction,test
