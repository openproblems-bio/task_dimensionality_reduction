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

# dimensionality_reduction 0.2.0 2024-12-19

## NEW FUNCTIONALITY

* Define waypoint cells during dataset processing for use by metrics (PR #11, PR #14)
* Add calculation of distances between waypoints to dataset preprocessing (PR #11, PR #14)
* Define label centroids in dataset preprocessing and calculate distances between centroids and from waypoints to centroids (PR #11, PR #14)
* Add a post-processing component that calculates distances in the embedding space (PR #11, PR #14)
* Add to centroid and between label distance correlation scores (PR #11, PR #14)

## MAJOR CHANGES

* Modify co-ranking metrics to use pre-computed distances (PR #11)
* Modify distance correlation metrics to use pre-computed distances (PR #11)
* Move spectral distance correlation to a separate component (PR #11)
* Disable the trustworthiness metric as it is calculated as part of the co-ranking metrics (PR #11)

## DOCUMENTATION

* Update documentation for distance correlation metrics (PR #11, PR #14)

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
