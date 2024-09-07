## VIASH START
par <- list(
  input = "resources_test/dimensionality_reduction/pancreas/dataset.h5ad",
  output = "output.h5ad",
  n_dim = 2
)
## VIASH END

message("Reading input files")
input <- anndata::read_h5ad(par$input)

message("Running destiny diffusion map")
# create SummarizedExperiment object
sce <- SingleCellExperiment::SingleCellExperiment(
  assays = list(
    logcounts = t(as.matrix(input$layers[["normalized"]]))
  )
)
dm <- destiny::DiffusionMap(sce)
X_emb <- destiny::eigenvectors(dm)[, seq_len(par$n_dim)]

message("Write output AnnData to file\n")
output <- anndata::AnnData(
  uns = list(
    dataset_id = input$uns[["dataset_id"]],
    normalization_id = input$uns[["normalization_id"]],
    method_id = meta$functionality_name
  ),
  obsm = list(
    X_emb = X_emb
  ),
  shape = input$shape
)
output$write_h5ad(par$output, compression = "gzip")
