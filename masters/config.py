from enum import Enum

from pathlib import Path

import typing

from pydantic import BaseModel, BaseSettings, ValidationError

from strictyaml import load, YAML

from masters import exceptions


ROOT = Path(__file__).resolve().parent
CONFIG_FILE_PATH = ROOT / "config.yml"
DATASET_DIR = ROOT / "datasets"


class FieldConfig(str, Enum):
    string = "string"


class MarshmallowValidation(str, Enum):
    ContainsNoneOf = "ContainsNoneOf"
    ContainsOnly = "ContainsOnly"
    Email = "Email"
    Equal = "Equal"
    Length = "Length"
    NoneOf = "NoneOf"
    OneOf = "OneOf"
    Predicate = "Predicate"
    Range = "Range"
    Regexp = "Regexp"
    URL = "URL"


class OneOfConfig(BaseModel):
    choices: typing.List[typing.Union[float, str]]
    labels: typing.Union[typing.List[str], None]


class RangeConfig(BaseModel):
    min: int
    max: int
    min_inclusive: typing.Union[bool, None] = True
    max_inclusive: typing.Union[bool, None] = True


class ValidationConfig(BaseModel):
    """Validation Custom Configuration Object"""

    name: str
    arguments: typing.Union[RangeConfig, OneOfConfig, None]


class ExtraConfig(BaseModel):
    """Missing Values"""

    missing: typing.Any = None
    allow_none: bool


class FeatureConfig(BaseModel):
    """Configuration for feature validation.

    Each feature will be validated using a particular schema, this config
    basically allows us to create the schema for the feature.
    """

    name: str
    field: str
    validation: typing.Union[ValidationConfig, None]
    extra_config: typing.Union[ExtraConfig, None]


class Config(BaseSettings):
    """Main configuration.

    The main configuration has information about the dataset location and can
    be used to store more if needed.
    """

    dataset_path: Path
    features: typing.List[FeatureConfig]


def find_config_file() -> Path:
    """Finds configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise FileNotFoundError(f"Configuration file was not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Path = None):
    """Parses the YAML configuration file"""
    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with cfg_path.open("r") as config_file:
            parsed_config = load(config_file.read())
            return parsed_config
    raise FileNotFoundError(f"Did not found config file at path {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config model"""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    try:
        _config = Config(**parsed_config.data)
    except ValidationError as err:
        raise exceptions.InvalidConfiguration(err)

    return _config


def get_all_features(config: Config) -> typing.List[str]:
    """Get all feature names from config file"""
    return [feature.name for feature in config.features]
