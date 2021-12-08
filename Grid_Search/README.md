# MER K8s Prototype - Classification Experiments

Contains all the scripts and results used to study audio and lyris music emotion classification into 4 quadrants. The final goal is to understand which are the best features, parameters and models to classify emotion, as well as the achieved performance.

The best results are then used to build the model to include in our prototype microservices.

Below is a description of the experiments and folders - updated as our experiments progress.

## Datasets
* The audio dataset contains 900 30s clips tagged into 4 quadrants (Russell) [add link and reference].
* The lyrics dataset consists of two of our previous datasets (771 + 180) tagged similarly [ref].

## Feature extraction and pre-processing
Audio features were extracted using the Essentia framework (add all the original features?). These were extracted from the original audio signals. In addition, we also extracted the same features from the the audio signals containing only vocals and only accompaniment - split with Spleeter by Deezer [ref].

The features were then pre-processed, cleaning features with no variance and deduplicating highly correlated ones [details in *tese do Tiago que só está em PT*]. The resulting feature matrices are available `datasets` folder:
* *original_after_correlation.csv* (from the original audio)
* *vocal_after_correlation.csv* (from the vocals only signal)
* *accompaniment_after_correlation.csv* (acompaniment only signal)
* *features_after_correlation.csv* (original+vocals+accompaniment deduplicated, keeping the features highly ranked according to chi2?).

Features from lyrics were extracted using the feature extraction tool available at [ref]
* *lyrics_features_after_correlation.csv*

## Scripts
TODO: brief description of the scripts
* `compute_ranking_(TuRF|chi2).py`
* `run_gridsearch.py`
* TODO: upload do script `test_selected_features.py`

## Results
Briefly describe the results folder...

