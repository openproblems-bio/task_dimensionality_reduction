#!/bin/bash

# get the root of the directory
REPO_ROOT=$(git rev-parse --show-toplevel)

# ensure that the command below is run from the root of the repository
cd "$REPO_ROOT"

set -e

echo "Running benchmark on test data"
echo "  Make sure to run 'scripts/project/build_all_docker_containers.sh'!"

# generate a unique id
RUN_ID="testrun_$(date +%Y-%m-%d_%H-%M-%S)"
publish_dir="temp/results/${RUN_ID}"

# write the parameters to file
cat > /tmp/params.yaml << HERE
id: cxg_mouse_pancreas_atlas
input_dataset: "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/dataset.h5ad"
input_solution: "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/solution.h5ad"
output_state: "state.yaml"
publish_dir: "$publish_dir"
HERE

nextflow run . \
  -main-script target/nextflow/workflows/run_benchmark/main.nf \
  -profile docker \
  -resume \
  -c common/nextflow_helpers/labels_ci.config \
  -params-file /tmp/params.yaml
