import os
import yaml


config_path = "/".join(os.path.abspath(__file__).split("/")[:-1])   + "/config.yaml"

with open(config_path, 'r') as stream:
    config = yaml.safe_load(stream)

output_folder = config["server"]["output_folder"]
g_cred_path = config["credentials"]["google"]
