import logging
import os
import socket

SUPPORTED_MONTHS = {
  '1' : '1mo',
  '3' : '3mo',
  '6' : '6mo',
  '12' : '1y',
}

SUPPORTED_TYPES = ["Open", "High", "Low", "Close"]

LOG_LEVELS = {
  'DEBUG' : 10,
  'INFO' : 20,  
  'WARNING' : 30,
  'ERROR' : 40,
  'CRITICAL' : 50
}

log_level =  LOG_LEVELS.get(os.environ.get('LOG_LEVEL','DEBUG'))
logger = None


class HostnameFilter(logging.Filter):
  hostname = socket.gethostname()

  def filter(self, record):
    record.hostname = HostnameFilter.hostname
    return True


def init_log():
  global logger

  # complete debugger info - useful for hypothetical test and prod envs
  if not logger:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.addFilter(HostnameFilter())
    formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(hostname)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(stream_handler)
    logger.setLevel(log_level)
    
  return logger