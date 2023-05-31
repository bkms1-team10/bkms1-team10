import logging
import logging.config

import sys
import traceback
import os
import json
import gzip
from datetime import datetime
import time
import pytz

# ----------------
# log utilities
global logger
logger = None


def init_logger():
    from ml import config
    global logger

    conf = config.conf['log']

    # make log folder
    curr_date = seconds_to_timestring(get_current_time_seconds(), '%Y-%m-%d')
    log_folder_name = 'stnd_ymd={0}'.format(curr_date)
    log_folder_path = os.path.join(config.LOGGING_DIRECTORY, log_folder_name)
    os.makedirs(log_folder_path, exist_ok=True)

    # logger config
    log_file_name = 'log.log'
    log_file_path = os.path.join(log_folder_path, log_file_name)

    conf['handlers']['file']['filename'] = log_file_path

    logging.config.dictConfig(conf)
    logger = logging.getLogger()
    sys.excepthook = handle_exception
    pass


def log_info(s):
    logger.info(s)
    pass


def log_error(s):
    logger.error(s)
    pass


def handle_exception(exc_type, exc_value, exc_traceback):
    ts = traceback.format_exception(exc_type, exc_value, exc_traceback)
    error_text = "".join(ts)

    log_error(error_text)
    pass
# ----------------


# # ----------------
# # file utilities
# 필요 없음
# def load_data(file_name, head):
#     count = 0
#     data = []
#     with gzip.open(file_name) as fin:
#         for l in fin:
#             d = json.loads(l)
#             count += 1
#             data.append(d)
#
#             # break if reaches the 100th line
#             if (head is not None) and (count > head):
#                 break
#     return data
# # ----------------


# ----------------
# time utilities
TIME_ZONE = None
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def _get_timezone():
    global TIME_ZONE

    if TIME_ZONE is None:
        TIME_ZONE = pytz.timezone('Asia/Seoul')
    return TIME_ZONE


def get_current_time_seconds():
    t = datetime.now(_get_timezone())
    return int(time.mktime(t.timetuple()))


def seconds_to_timestring(seconds, format_string=TIME_FORMAT):
    return datetime.fromtimestamp(seconds).strftime(format_string)
# ----------------
