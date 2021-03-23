import pytest


VALID_FEATURE_CONFIG = """
dataset_path: {dataset_path}
features:
  - name: feature-1
    field: string
    extra_config:
      allow_none: True
"""
INVALID_FEATURE_CONFIG = """
dataset_path: {dataset_path}
features:
  - name: feature-1
"""


@pytest.fixture
def valid_yaml(tmp_path):
    directory = tmp_path / "config"
    directory.mkdir()

    dataset_file = directory / "dataset.csv"
    dataset_file.touch()

    yaml_file = directory / "config.yml"
    yaml_file.write_text(VALID_FEATURE_CONFIG.format(dataset_path=dataset_file))

    return yaml_file


@pytest.fixture
def invalid_yaml(tmp_path):
    directory = tmp_path / "config"
    directory.mkdir()

    dataset_file = directory / "dataset.csv"
    dataset_file.touch()

    yaml_file = directory / "config.yml"
    yaml_file.write_text(INVALID_FEATURE_CONFIG.format(dataset_path=dataset_file))

    return yaml_file
