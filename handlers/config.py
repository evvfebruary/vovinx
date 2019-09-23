import os
import re
import psutil
from handlers.io_handlers import open_io
from handlers.logger import logger


def read_config(config_path):
    default_config = {
        "address": '0.0.0.0',
        "port": 80,
        "queue": 8,
        "datasize": 1024,
        "cpu_limit": psutil.cpu_count(),
        "document_root": "/server/"
    }
    file_existed = os.path.exists(config_path)
    if not file_existed:
        raise ValueError(f"Missed config on {config_path}")
    config_raw, error = open_io(config_path)
    if error:
        raise ValueError(f"Read file error:  {config_path}")
    config_values = config_raw.decode("utf-8").split('\n')
    for values in config_values:
        if values:
            key, value = re.search(r'\S* \S*', values).group(0).split(' ')
            default_config.update({key: value})
    default_config["binding"] = (default_config["address"], default_config["port"])
    default_config["cpu_limit"] = int(default_config["cpu_limit"])
    logger.info(f"Config: {default_config}")
    return default_config
