library(anndata)
library(coRanking)

## VIASH START
par <- list(
  "input_embedding" = "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/processed_embedding.h5ad",
  "input_solution" = "resources_test/task_dimensionality_reduction/cxg_mouse_pancreas_atlas/solution.h5ad",
  "output" = "score.h5ad"
)
## VIASH END

message("Read anndata objects")
input_solution <- anndata::read_h5ad(par[["input_solution"]])
input_embedding <- anndata::read_h5ad(par[["input_embedding"]])

# Get datasets
dist_highdim <- input_solution$uns[["between_waypoint_distances"]]
dist_emb <- input_embedding$uns[["between_waypoint_distances"]]

if (any(is.na(dist_emb))) {
  continuity_at_k30 <- 0
  trustworthiness_at_k30 <- 0
  qnx_at_k30 <- 0
  lcmc_at_k30 <- 0
  qnx_auc <- 0
  qlocal <- 0
  qglobal <- 0
} else {
  message("Compute ranking matrices")
  rmat_highdim <- rankmatrix(dist_highdim, input = "dist")
  rmat_emb <- rankmatrix(dist_emb, input = "dist")

  message("Compute coranking matrix")
  corank <- coranking(rmat_highdim, rmat_emb, "rank")

  message("Compute metrics")
  # Compute QNX. This is a curve indicating the percentage of points
  # that are mild in- and extrusions or keep their rank.
  qnx <- Q_NX(corank)

  # Calculate the local continuity meta-criterion from a co-ranking matrix.
  lcmc <- LCMC(corank)

  # The values of qnx are split into local and global values by kmax
  kmax <- which.max(lcmc)

  # Check certain quality values at k=30
  k30 <- 30
  trustworthiness_at_k30 <- coRanking:::cm.M_T(corank, k30)
  continuity_at_k30 <- coRanking:::cm.M_C(corank, k30)
  qnx_at_k30 <- qnx[[k30]]
  lcmc_at_k30 <- lcmc[[k30]]

  # Area under the QNX curve
  qnx_auc <- mean(qnx)

  # Local quality measure
  qlocal <- mean(qnx[seq_len(kmax)])

  # Global quality measure
  qglobal <- mean(qnx[-seq_len(kmax)])
}

message("Construct output AnnData")
output <- AnnData(
  shape = c(0L, 0L),
  uns = list(
    dataset_id = input_solution$uns[["dataset_id"]],
    normalization_id = input_solution$uns[["normalization_id"]],
    method_id = input_embedding$uns[["method_id"]],
    metric_ids = c(
      "continuity_at_k30",
      "trustworthiness_at_k30",
      "qnx_at_k30",
      "lcmc_at_k30",
      "qnx_auc",
      "qlocal",
      "qglobal"
    ),
    metric_values = c(
      continuity_at_k30,
      trustworthiness_at_k30,
      qnx_at_k30,
      lcmc_at_k30,
      qnx_auc,
      qlocal,
      qglobal
    )
  )
)
print(output)

message("Write to file")
output$write_h5ad(par$output)
