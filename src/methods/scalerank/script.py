import anndata as ad
import numpy as np
import scanpy as sc
from scalerank import ScaleRank
from sklearn.neighbors import NearestNeighbors

## VIASH START
par = {
    "input": "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/dataset.h5ad",
    "output": "reduced.h5ad",
    "n_hvg": 3000,
    "n_pca_dims": 100,
    "gamma": 0.5,
    "dens_lambda": 4.0,
    "dens_pca_dims": 300,
}
meta = {
    "name": "scalerank",
}
## VIASH END

DENS_K = 30  # neighbours that define a local radius (ScaleRank's dens_k)


def pca(X, n_comps):
    n_comps = min(n_comps, min(X.shape) - 1)
    return np.ascontiguousarray(sc.tl.pca(X, n_comps=n_comps, svd_solver="arpack"), dtype=np.float64)


def log_radii(Z, k):
    """Log of the mean squared distance to each point's k nearest neighbours."""
    k = min(k, Z.shape[0] - 1)
    dist, _ = NearestNeighbors(n_neighbors=k + 1).fit(Z).kneighbors(Z)
    return np.log(np.maximum((dist[:, 1:].astype(np.float64) ** 2).mean(axis=1), 1e-300))


print("Load input data", flush=True)
input = ad.read_h5ad(par["input"])
X_mat = input.layers["normalized"]

X_rank = X_mat
if par["n_hvg"]:
    print(f"Select top {par['n_hvg']} highly variable genes", flush=True)
    idx = input.var["hvg_score"].to_numpy().argsort()[::-1][: par["n_hvg"]]
    X_rank = X_mat[:, idx]

print(f"Apply PCA ({par['n_pca_dims']} dimensions) for the neighbour ranks", flush=True)
Z = pca(X_rank, par["n_pca_dims"])

target = None
if par["dens_lambda"] > 0 and par["dens_pca_dims"]:
    print(f"Measure target local radii on PCA ({par['dens_pca_dims']} dimensions) of all genes", flush=True)
    target = log_radii(pca(X_mat, par["dens_pca_dims"]), DENS_K)

print("Run ScaleRank", flush=True)
X_emb = ScaleRank(
    gamma=par["gamma"],
    dens_lambda=par["dens_lambda"],
    dens_k=DENS_K,
    random_state=42,
).fit_transform(Z, dens_target=target)

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
