import anndata as ad
import numpy as np
from sklearn.metrics import pairwise_distances

## VIASH START
par = {
    "input_embedding": "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/embedding.h5ad",
    "input_solution": "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/solution.h5ad",
    "output_embedding": "processed_embedding.h5ad",
}
## VIASH END

print("====== Embedding processor ======", flush=True)

print("\n>>> Reading solution...", flush=True)
solution = ad.read_h5ad(par["input_solution"])
print(solution, flush=True)

print("\n>>> Reading embedding...", flush=True)
adata = ad.read_h5ad(par["input_embedding"])
# Make sure cells have the same order
adata = adata[solution.obs_names, :].copy()
print(adata, flush=True)

print("\n>>> Calculating distances to waypoints...", flush=True)
adata.obsm["waypoint_distances"] = pairwise_distances(
    adata.obsm["X_emb"],
    adata.obsm["X_emb"][solution.obs["is_waypoint"].values, :],
    metric="euclidean",
    n_jobs=-2,
)
np.fill_diagonal(adata.obsm["waypoint_distances"], 0)

print("\n>>> Calculating distances between waypoints...", flush=True)
adata.uns["between_waypoint_distances"] = pairwise_distances(
    adata.obsm["X_emb"][solution.obs["is_waypoint"].values, :],
    adata.obsm["X_emb"][solution.obs["is_waypoint"].values, :],
    metric="euclidean",
    n_jobs=-2,
)
np.fill_diagonal(adata.uns["between_waypoint_distances"], 0)

print("\n>>> Calculating label centroids...", flush=True)
emb_mat = adata.obsm["X_emb"]
labels = np.unique(solution.obs["cell_type"])
centroids = np.zeros((len(labels), emb_mat.shape[1]))
for i, label in enumerate(labels):
    is_label = solution.obs["cell_type"] == label
    centroids[i, :] = np.mean(emb_mat[is_label, :], axis=0)

adata.uns["label_centroids"] = centroids

print("\n>>> Calculating distances to centroids...", flush=True)
adata.obsm["centroid_distances"] = pairwise_distances(
    adata.obsm["X_emb"], centroids, metric="euclidean", n_jobs=-2
)
np.fill_diagonal(adata.obsm["centroid_distances"], 0)

print("\n>>> Calculating distances between centroids...", flush=True)
adata.uns["between_centroid_distances"] = pairwise_distances(
    centroids, centroids, metric="euclidean", n_jobs=-2
)
np.fill_diagonal(adata.uns["between_centroid_distances"], 0)

print("\n>>> Writing processed embedding...", flush=True)
print(adata, flush=True)
adata.write_h5ad(par["output"])
print(f"Output dataset file: '{par['output']}'", flush=True)

print("\n>>> Done!", flush=True)
