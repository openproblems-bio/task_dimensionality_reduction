import anndata as ad
import scanpy as sc
from umap import UMAP

## VIASH START
par = {
    "input": "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/train.h5ad",
    "output": "reduced.h5ad",
    "n_pca_dims": 50,
    "n_hvg": 1000,
}
meta = {
    "name": "densmap",
}
## VIASH END

print("Load input data", flush=True)
input = ad.read_h5ad(par["input"])
X_mat = input.layers["normalized"]

if par["n_hvg"]:
    print(f"Select top {par['n_hvg']} high variable genes", flush=True)
    idx = input.var["hvg_score"].to_numpy().argsort()[::-1][: par["n_hvg"]]
    X_mat = X_mat[:, idx]

if par["n_pca_dims"]:
    print("Apply PCA to normalized data", flush=True)
    umap_input = sc.tl.pca(X_mat, n_comps=par["n_pca_dims"], svd_solver="arpack")
else:
    print("Use normalized data as input for UMAP", flush=True)
    umap_input = X_mat

print("Run densMAP", flush=True)
X_emb = UMAP(densmap=True, random_state=42).fit_transform(umap_input)

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
