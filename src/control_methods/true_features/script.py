import anndata as ad

## VIASH START
par = {
    "input": "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/test.h5ad",
    "output": "reduced.h5ad",
}
meta = {
    "name": "true_features",
}
## VIASH END

print("Load input data", flush=True)
input = ad.read_h5ad(par["input"])

print("Create high dimensionally embedding with all features", flush=True)
X_emb = input.layers["normalized"].toarray()

print("Create output AnnData", flush=True)
output = ad.AnnData(
    obs=input.obs[[]],
    obsm={"X_emb": X_emb},
    uns={
        "dataset_id": input.uns["dataset_id"],
        "normalization_id": input.uns["normalization_id"],
        "method_id": meta["name"],
    },
)

print("Write output to file", flush=True)
output.write_h5ad(par["output"], compression="gzip")
