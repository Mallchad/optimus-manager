import sys
import os
from pathlib import Path
import logging
from . import envs


def set_logger_config(log_type, log_id):

    log_dir_path = Path(envs.LOG_DIR_PATH)
    log_filepath = log_dir_path / log_type / ("%s-%d.log" % (log_type, log_id))

    os.makedirs(log_filepath.parent, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="[%(relativeCreated)d] %(levelname)s: %(message)s",
        handlers=[
            logging.StreamHandler(stream=sys.stdout),
            logging.FileHandler(filename=log_filepath)
        ]
    )

def get_logger():
    return logging.getLogger()
