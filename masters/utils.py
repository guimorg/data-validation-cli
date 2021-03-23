import csv

from pathlib import Path

import pandas as pd

from numpy import nan

from masters.config import get_all_features

LOCAL_PATH = Path.cwd()
RESULTS_PATH = LOCAL_PATH / "results.csv"
FEATURES_PATH = LOCAL_PATH / "features.csv"


def load_dataset(config_model):
    """Loads dataset for processing"""
    file_path = Path(config_model.dataset_path)
    features = get_all_features(config_model)
    features = set(features) | {"age"}
    # Pandas has an easier interface to read CSV data, especically when the
    # pattern is a little weird, RedCap is one of these cases
    dataset = pd.read_csv(file_path, usecols=features, low_memory=True)

    # NOTE: we have to fitler **without** using a schema because there are some
    # issues with how the dataset is stored on RedCap.
    dataset.dropna(subset=["age"], inplace=True)
    dataset.replace({nan: None}, inplace=True)  # marshmallow validation
    # dataset.drop(["age"], axis=1, inplace=True)

    return dataset.to_dict("records")


def write_results(results):
    """Writes result on csv file."""
    with RESULTS_PATH.open("w") as writer:
        csvwriter = csv.writer(writer)
        csvwriter.writerows(results)


def write_features(config_file):
    """Writes features on CSV file."""
    features = get_all_features(config_file)
    with FEATURES_PATH.open("w") as writer:
        for feature in features:
            writer.write(f"{feature}\n")
