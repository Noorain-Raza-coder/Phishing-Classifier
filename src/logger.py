import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.getcwd() , "logs")
FILE_PATH = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR , FILE_PATH)

os.makedirs(LOG_FILE_PATH , exist_ok=True)

FULL_LOG_FILE_PATH = os.path.join(LOG_FILE_PATH , FILE_PATH)


logging.basicConfig(
    filename=FULL_LOG_FILE_PATH,
    format= "[%(asctime)s] %(lineno)s %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO

)