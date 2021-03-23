from pathlib import Path

import pytest

from strictyaml import YAML

from masters import config, exceptions


def test_fetch_config_from_yaml(valid_yaml):
    # Given
    yaml_file = valid_yaml

    # When
    config_yaml = config.fetch_config_from_yaml(yaml_file)

    # Then
    assert isinstance(config_yaml, YAML)


def test_fetch_config_from_yaml_not_exist(valid_yaml):
    # Given
    yaml_file = Path(__file__).parent / "config.yml"

    # When, Then
    with pytest.raises(FileNotFoundError):
        _ = config.fetch_config_from_yaml(yaml_file)


def test_create_and_validate_config(valid_yaml):
    # Given
    yaml_file = valid_yaml

    # When
    parsed_config = config.fetch_config_from_yaml(yaml_file)
    config_yaml = config.create_and_validate_config(parsed_config)

    # Then
    assert isinstance(config_yaml, config.Config)


def test_create_and_validate_config_invalid(invalid_yaml):
    # Given
    yaml_file = invalid_yaml

    # When, Then
    parsed_config = config.fetch_config_from_yaml(yaml_file)
    with pytest.raises(exceptions.InvalidConfiguration):
        _ = config.create_and_validate_config(parsed_config)
