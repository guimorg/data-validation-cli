from pathlib import Path

import time

import click

import emoji

from masters import config, validation, utils


@click.command()
@click.argument("config_path", type=click.Path())
def cli(config_path):
    """\b
        __  ___           __
       /  |/  /___ ______/ /____  __________
      / /|_/ / __ `/ ___/ __/ _ \\/ ___/ ___/
     / /  / / /_/ (__  ) /_/  __/ /  (__  )
    /_/  /_/\\__,_/____/\\__/\\___/_/  /____/

    Helper CLI to validate data for your masters degree!

    CONFIG_PATH refers to the configuration file path for the masters
    validation job.
    """
    click.echo(
        emoji.emojize(":blush:  Starting process for validation...", use_aliases=True)
    )
    click.echo(
        emoji.emojize(":mag:  Looking for the configuration YAML...", use_aliases=True)
    )

    parsed_config = config.fetch_config_from_yaml(Path(config_path))
    config_model = config.create_and_validate_config(parsed_config)
    click.echo(emoji.emojize(":eyes:  Creating validation schema", use_aliases=True))
    schema = validation.schema_factory(configuration_dict=config_model.dict())

    click.echo(emoji.emojize(":mag:  Reading dataset...", use_aliases=True))
    dataset = utils.load_dataset(config_model)

    click.echo(
        emoji.emojize(":flushed:  Starting validation process...", use_aliases=True)
    )
    click.echo(
        emoji.emojize(":sweat_smile:  This could take a while...", use_aliases=True)
    )
    tic = time.time()
    errors = validation.validate_inputs(input_data=dataset, validation_schema=schema)
    elapsed_time = time.time() - tic

    click.echo(
        emoji.emojize(
            f":alarm_clock:  Process took {elapsed_time} s...", use_aliases=True
        )
    )
    click.echo(emoji.emojize(":pencil:  Writing result on ...", use_aliases=True))
    utils.write_results(results=errors)
    utils.write_features(config_file=config_model)
