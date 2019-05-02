import pandas as pd
import psutil
import os
import argparse
from subprocess import Popen
from multiprocessing import Pool, Queue
import logging
from logging.handlers import QueueHandler, QueueListener
import traceback
from timeit import default_timer as timer
import datetime
from itertools import repeat
import schedule
import time
import yaml

from db_utils import Database_obj

__author__ = "StevenGuarino"
__version__ = "0.1"

# use mysql datetime format to prevent db insertion errors
time.strftime('%Y-%m-%d %H:%M:%S')

"""
TODOs:
  * currently not using --time_zone
  * parallel processing not working on alex server
"""

class Sys_poll():
  def __init__(self,
               config_args):
    self.config_args = config_args
    self.log_dir = os.path.join(os.path.curdir, self.config_args["log_dir"])
    self.table_names = self.config_args["db_table_name"]
    self.delete_interval = self.config_args["delete_interval"]
    self.metrics = self.config_args["metrics"]
    self.logger, self.queue_listener, self.queue = self.logger_init(self.log_dir,
                                                                    filename="sys_poll")
    self.poll_db = Database_obj(host=self.config_args["db_host"],
                                port=self.config_args["db_port"],
                                user=self.config_args["db_username"],
                                password=self.config_args["db_password"],
                                database=self.config_args["db_name"],
                                keep_existing=self.config_args["keep_existing"],
                                logger=self.logger)
  # end

  def get_processes(self):
    """
    desc: fetch process ids
    returns: pids for all running processes
    """
    return [p.pid for p in psutil.process_iter() if isinstance(p.pid, int)]
  # end

  def get_process_metrics(self,
                          args):
    """
    desc: get metrics for a given process id
    args:
      unpacks to:
        pid: process id (str)
        metrics: metrics to pull
    returns: dict of metrics for a process id
    """
    pid, metrics = args
    p_metrics = {metric: getattr(pid, metric)() for metric in metrics if hasattr(pid, metric)}
    p_metrics["nowtime"] = str(datetime.datetime.now())
    p_metrics["pid"] = pid.pid
    return p_metrics
  # end

  def worker_init(self,
                  queue):
    """
    desc: init for worker for logging during multiprocessing
    args:
      queue: queue for logging
    """
    # all records from worker processes go to qh and then into q
    queue_handler = QueueHandler(queue)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)
  # end

  def logger_init(self,
                  path,
                  filename):
    """
    desc: create logger
    args:
      path: path to logging directory
      filename: log filename
    returns:
      logger
      queue_listener
      queue
    """
    queue = Queue()
    # handler for all log records
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(asctime)s - %(process)s - %(message)s"))

    # queue_listener gets records from the queue and sends them to the handler
    queue_listener = QueueListener(queue, handler)
    queue_listener.start()

    # currentTime = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    if not os.path.exists(path):
      os.mkdir(path)
    logFileName = os.path.join(path, "{}.log".format(filename))
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename=logFileName,
                        filemode='w')

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)
    # add the handler to the logger so records from this process are handled
    logger.addHandler(handler)

    return logger, queue_listener, queue
  # end

  def main(self):
    """
    desc: get system information by process
    returns: pandas dataframe with system metrics by process id
    """
    pids = list(map(int, self.get_processes()))
    process_objs = [psutil.Process(pid) for pid in pids]

    all_process_metrics = [self.get_process_metrics([process_objs, metrics_])
                              for process_objs, metrics_ in list(zip(process_objs, repeat(self.metrics, len(process_objs))))]
    all_process_metrics = pd.DataFrame(all_process_metrics)

    if not self.poll_db.check_table_exists(self.table_names):
      cols = [] # TODO add unique identifier
      for key in all_process_metrics.keys():
        if key == "nowtime": cols.append(str(key) + " datetime")
        else: cols.append(str(key) + " varchar(255)")
      cols = ", ".join(cols)
      self.poll_db.create_table(self.table_names, cols) # create current table

    keys = list(all_process_metrics.keys())
    vals = list(zip(*[all_process_metrics[k].values.tolist() for k in keys]))
    self.poll_db.insert_into_table(self.table_names,
                                   ", ".join(keys),
                                   vals)
    self.poll_db.delete_from_table(self.table_names,
                                   "nowtime",
                                   self.delete_interval)
  # end
# end

if __name__ == "__main__":
  args = yaml.safe_load(open("sys_poll.yml", "r"))
  sys_poll_obj = Sys_poll(args)
  schedule.every(args["poll_every"]).seconds.do(sys_poll_obj.main)

  while True:
    try:
      schedule.run_pending()
      time.sleep(args["poll_every"])
    except Exception as e:
      sys_poll_obj.logger.error(e)
      time.sleep(args["poll_every"])
      pass
