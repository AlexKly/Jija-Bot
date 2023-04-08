import os, pathlib
from src.utils.load_configs import load_configs

DIR_PROJECT = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent
DIR_CONFIGS = DIR_PROJECT/'configs'
DIR_DATA = DIR_PROJECT/'data'
DIR_IMAGES = DIR_DATA/'images'
DIR_AUDIO = DIR_DATA/'audio'
DIR_MODELS = DIR_PROJECT/'models'
DIR_BERT = DIR_MODELS/'bert'
DIR_ST_MODEL = DIR_MODELS/'st_model'
PATH_BOT_YAML = DIR_PROJECT/'bot.yaml'
PATH_DATA_INFO_YAML = DIR_DATA/'data_info.yaml'

BOT_CONFIGS = load_configs(path=PATH_BOT_YAML)
DATA_INFO = load_configs(path=PATH_DATA_INFO_YAML)
