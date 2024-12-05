import anndata as ad
import scipy.spatial
import scipy.stats
import sklearn.decomposition

## VIASH START
par = {
    "input_embedding": "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/processed_embedding.h5ad",
    "input_solution": "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/solution.h5ad",
    "output": "score.h5ad",
}
## VIASH END


def _distance_correlation(X, X_emb):
    high_dimensional_distance_vector = scipy.spatial.distance.pdist(X)
    low_dimensional_distance_vector = scipy.spatial.distance.pdist(X_emb)
    corr = scipy.stats.spearmanr(
        low_dimensional_distance_vector, high_dimensional_distance_vector
    )
    return corr


print("Load data", flush=True)
input_solution = ad.read_h5ad(par["input_solution"])
input_embedding = ad.read_h5ad(par["input_embedding"])

high_dim = input_solution.layers["normalized"]
X_emb = input_embedding.obsm["X_emb"]

print("Compute NNLS residual after SVD", flush=True)
n_svd = 500
svd_emb = sklearn.decomposition.TruncatedSVD(n_svd).fit_transform(high_dim)
dist_corr = _distance_correlation(svd_emb, X_emb).correlation

print("Create output AnnData object", flush=True)
output = ad.AnnData(
    uns={
        "dataset_id": input_solution.uns["dataset_id"],
        "normalization_id": input_solution.uns["normalization_id"],
        "method_id": input_embedding.uns["method_id"],
        "metric_ids": ["distance_correlation"],
        "metric_values": [dist_corr],
    }
)

print("Write data to file", flush=True)
output.write_h5ad(par["output"], compression="gzip")
