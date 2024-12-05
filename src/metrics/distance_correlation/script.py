import anndata as ad
import scipy

## VIASH START
par = {
    "input_embedding": "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/processed_embedding.h5ad",
    "input_solution": "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/solution.h5ad",
    "output": "score.h5ad",
}
## VIASH END

print(f"====== Distance correlation metrics (scipy v{scipy.__version__}) ======", flush=True)

print("\n>>> Reading solution...", flush=True)
solution = ad.read_h5ad(par["input_solution"])
print(solution, flush=True)

print("\n>>> Reading embedding...", flush=True)
embedding = ad.read_h5ad(par["input_embedding"])
print(embedding, flush=True)

print("\n>>> Calculating waypoint distance correlation..", flush=True)
high_dists = solution.obsm["waypoint_distances"]
emb_dists = embedding.obsm["waypoint_distances"]
waypoint_corr = scipy.stats.spearmanr(high_dists, emb_dists, axis=None).correlation
print(f"Waypoint distance correlation: {waypoint_corr}", flush=True)

print("\n>>> Calculating centroid distance correlation..", flush=True)
high_dists = solution.obsm["centroid_distances"]
emb_dists = embedding.obsm["centroid_distances"]
centroid_corr = scipy.stats.spearmanr(high_dists, emb_dists, axis=None).correlation
print(f"Centroid distance correlation: {centroid_corr}", flush=True)

print("\n>>> Creating output AnnData object...", flush=True)
output = ad.AnnData(
    uns={
        "dataset_id": solution.uns["dataset_id"],
        "normalization_id": solution.uns["normalization_id"],
        "method_id": embedding.uns["method_id"],
        "metric_ids": ["waypoint_distance_correlation", "centroid_distance_correlation"],
        "metric_values": [waypoint_corr, centroid_corr],
    }
)
print(output, flush=True)

print("\n>>> Writing output file...", flush=True)
output.write_h5ad(par["output"], compression="gzip")
print(f"Output file: '{par['output']}'", flush=True)

print("\n>>> Done!", flush=True)
