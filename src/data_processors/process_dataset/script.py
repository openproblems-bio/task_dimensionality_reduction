import sys

import anndata as ad
import openproblems as op

## VIASH START
par = {
    "input": "resources_test/common/pancreas/dataset.h5ad",
    "obs_label": "cell_type",
    "var_hvg_score": "hvg_score",
    "output_dataset": "train.h5ad",
    "output_solution": "test.h5ad",
}
meta = {
    "resources_dir": "target/executable/data_processors/process_dataset",
    "config": "target/executable/data_processors/process_dataset/.config.vsh.yaml",
}
## VIASH END


# import helper functions
sys.path.append(meta["resources_dir"])
from subset_h5ad_by_format import subset_h5ad_by_format

config = op.project.read_viash_config(meta["config"])

print(">> Load Data", flush=True)
adata = ad.read_h5ad(par["input"])

print(adata)

# Subset the different adatas
print(">> Figuring which data needs to be copied to which output file", flush=True)
# Use par arguments to look for values in different slots
slot_mapping = {
    "obs": {
        "label": par["obs_label"],
    },
    "var": {
        "hvg_score": par["var_hvg_score"],
    },
}

print(">> Creating input data", flush=True)
output_dataset = subset_h5ad_by_format(adata, config, "output_dataset", slot_mapping)

print(">> Creating solution data", flush=True)
output_solution = subset_h5ad_by_format(adata, config, "output_solution", slot_mapping)

print(">> Writing data", flush=True)
output_dataset.write_h5ad(par["output_dataset"])
output_solution.write_h5ad(par["output_solution"])
