import sys
import logging
from datetime import datetime
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
            log_record['name'] = "stakater-network-logger"


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logHandler = logging.StreamHandler(sys.stdout)
    # formatter = jsonlogger.JsonFormatter()
    formatter = CustomJsonFormatter('%(timestamp)s %(name)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    return logger


# logger.info({"special": "value", "run": 12})