<!-- # dimensionality_reduction x.y.z

## BREAKING CHANGES

* Restructured `src` directory (PR #3).

## NEW FUNCTIONALITY

* Added `control_methods/true_labels` component (PR #5).
* Added `methods/logistic_regression` component (PR #5).
* Added `metrics/accuracy` component (PR #5).

## MAJOR CHANGES

* Updated `api` files (PR #5).
* Updated configs, components and CI to the latest Viash version (PR #8).

## MINOR CHANGES

* Updated `README.md` (PR #5).

## BUGFIXES -->

# dimensionality_reduction 0.2.0 2024-12-09

## NEW FUNCTIONALITY

* Add calculation of distances to/between waypoints and label centroids to dataset pre-processing
* Add a post-processing component that calculates distances in the embedding space
* Add to centroid and between label distance correlation scores

## MAJOR CHANGES

* Modify co-ranking metrics to use pre-computed distances
* Modify distance correlation metrics to use pre-computed distances
* Move spectral distance correlation to a separate component
* Disable the trustworthiness metric as it is calculated as part of the co-ranking metrics

## DOCUMENTATION

* Update documentation for distance correlation metrics

## MINOR CHANGES

* Speed up calculating distance matrices in the co-ranking metrics (PR #4)

# dimensionality_reduction 0.1.3 2024-10-09

## MINOR CHANGES

* Speed up calculating distance matrices in the co-ranking metrics (PR #4)

# dimensionality_reduction 0.1.2 2024-09-23

## MINOR CHANGES

* Updated workflow resources for method and metric components (PR #3)

# dimensionality_reduction 0.1.1 2024-09-18

## NEW FUNCTIONALITY

* Updated workflows to work correctly for this task (PR #2)

# dimensionality_reduction 0.1.0 2024-09-05

## NEW FUNCTIONALITY

* Migrated components from the main Open Problems repository (PR #1)
