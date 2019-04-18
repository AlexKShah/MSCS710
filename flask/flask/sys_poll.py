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

from db_utils import database_obj

__author__ = "StevenGuarino"
__version__ = "0.1"

"""
TODOs:
  * currently not using --time_zone
  * add error handling
  * parallel processing not working on alex server
"""

def get_args():
  """
  desc: get cli arguments
  returns:
  args: dictionary of cli arguments
  """
  parser = argparse.ArgumentParser(description="this script pull sys information")
  parser.add_argument("--poll_every",
                      help="how often (seconds) to poll system information",
                      type=int,
                      default=10)
  parser.add_argument("--time_zone",
                      help="specify the time zone of the machine to gather sys information from",
                      type=str,
                      default="America/New_York")
  parser.add_argument("--log_dir",
                      help="directory to write logs to",
                      type=str,
                      default="logs")
  parser.add_argument("--process_in_parallel",
                      help="use parallel processing where appropiate",
                      type=bool,
                      default=False)
  parser.add_argument("--poll_db",
                      help="database to write recently polled data",
                      type=str,
                      default="poll")
  parser.add_argument("--keep_existing",
                      help="keep existing database",
                      type=bool,
                      default=False)
  parser.add_argument("--db_username",
                      help="database user name",
                      type=str,
                      default="root")
  parser.add_argument("--db_password",
                      help="database password",
                      type=str,
                      default="alex")
  args = parser.parse_args()
  return args
# end

class sys_poll():
  def __init__(self,
               cli_args):
    self.cli_args = cli_args
    self.table_names = "current"
    self.poll_db = database_obj(user=self.cli_args["db_username"],
                                password=self.cli_args["db_password"],
                                database=self.cli_args["poll_db"],
                                keep_existing=self.cli_args["keep_existing"])
  # end

  def get_processes(self):
    """
    desc: fetch process ids
    returns: pids for all running processes
    """
    return [pid for pid in os.listdir("/proc") if pid.isdigit()]
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
    logger, queue_listener, queue = self.logger_init(os.path.join(os.getcwd(), self.cli_args["log_dir"]),
                                                     filename="sys_poll")
    """
    note: to add more metrics simply go through https://psutil.readthedocs.io/en/latest/
          find methods on Process object and add to `metrics` list below
    """
    metrics = ["memory_percent",
               "cpu_percent",
               "num_threads",
               "name"] # list of metrics to call on psutil.Process object
    pids = list(map(int, self.get_processes()))
    process_objs = [psutil.Process(pid) for pid in pids]

    if self.cli_args["process_in_parallel"]:
      pool = Pool(os.cpu_count(), self.worker_init, [queue])
      all_process_metrics = [process_metrics for process_metrics in pool.map(self.get_process_metrics, list(zip(process_objs, repeat(metrics, len(process_objs)))))]
      pool.close()
      pool.join()
      queue_listener.stop()
    else:
      all_process_metrics = [self.get_process_metrics([process_objs, metrics_])
                              for process_objs, metrics_ in list(zip(process_objs, repeat(metrics, len(process_objs))))]
    all_process_metrics = pd.DataFrame(all_process_metrics)

    if not self.poll_db.check_table_exists(self.table_names):
      cols = [] # TODO add unique identifier
      for key in all_process_metrics.keys():
        if key == "nowtime": cols.append(str(key) + " datetime")
        else: cols.append(str(key) + " varchar(255)")
      cols = ", ".join(cols)
      self.poll_db.create_table(self.table_names, cols) # create current table

    keys = list(all_process_metrics.keys())
    #vals = list(all_process_metrics.itertuples(index=False, name=None))
    vals = list(zip(*[all_process_metrics[k].values.tolist() for k in keys]))
    self.poll_db.insert_into_table(self.table_names,
                                   ", ".join(keys),
                                   vals)
  # end
# end

if __name__ == "__main__":
  args = get_args()
  sys_poll_obj = sys_poll(vars(args))

  schedule.every(args.poll_every).seconds.do(sys_poll_obj.main)

  while True:
    schedule.run_pending()
    time.sleep(1)
