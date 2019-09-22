import os
import psutil
from handlers.io_handlers import open_io

default_config = {
    "address": '0.0.0.0',
    "port": 80,
    "queue": 8,
    "datasize": 1024,
    "cpu_count": psutil.cpu_count(),
    "document_root": "/server/"
}


def read_config(config_path):
    file_existed = os.path.exists(config_path)
    if not file_existed:
        raise ValueError(f"Missed config on {config_path}")
    config_raw, error = open_io(config_path)
    if error:
        raise ValueError(f"Read file error:  {config_path}")
    for line in config_raw.decode("utf-8").split("\n"):
        for only_values in line.split("#")[:-1]:
            try:
                key, value = [value for value in only_values.split(" ") if len(value) >= 1]
            except ValueError as config_error:
                raise ValueError("Wrong config format")
            default_config.update({key: value})
    default_config["binding"] = (default_config["address"], default_config["port"])
    default_config["cpu_limit"] = int(default_config["cpu_limit"])
    return default_config
