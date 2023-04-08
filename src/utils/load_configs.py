import yaml, pathlib


def load_configs(path: pathlib.Path):
    """ Load configuration from yaml file.

    :param path: Path to yaml file with configurations.
    :return: Parsed dict from yaml file.
    """
    with path.open('r', encoding='utf-8') as yaml_f:
        return yaml.safe_load(yaml_f)
