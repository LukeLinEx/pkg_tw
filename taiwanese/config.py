import yaml


config_path = "/home/ubuntu/pkg_tw/taiwanese/config.yaml"


with open(config_path, 'r') as stream:
    config = yaml.safe_load(stream)

output_folder = config["server"]["output_folder"]
g_cred_path = config["credentials"]["google"]
