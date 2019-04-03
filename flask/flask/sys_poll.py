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

__author__ = "StevenGuarino"
__version__ = "0.1"

"""
TODOs:
  currently not using --time_zone
  not putting items in database yet
  add error handling
"""

def get_args():
  """
  desc: get cli arguments
  returns:
  args: dictionary of cli arguments
  """
  parser = argparse.ArgumentParser(description="this script pull sys information")
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
                      default=True)
  args = parser.parse_args()
  return args
# end

def get_processes():
  """
  desc: fetch process ids
  returns: pids for all running processes
  """
  return [pid for pid in os.listdir("/proc") if pid.isdigit()]
# end

def get_process_metrics(args):
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
  p_metrics["current_time"] = str(datetime.datetime.now())
  p_metrics["pid"] = pid.pid
  return p_metrics
# end

def worker_init(queue):
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

def logger_init(path, filename):
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

def sys_poll_main():
  """
  desc: get system information by process
  returns: pandas dataframe with system metrics by process id
  """
  args = get_args()
  logger, queue_listener, queue = logger_init(path=os.path.join(os.getcwd(), args.log_dir),
                                              filename="sys_poll")
  """
  note: to add more metrics simply go through https://psutil.readthedocs.io/en/latest/
        find methods on Process object and add to `metrics` list below
  """
  metrics = ["memory_percent",
             "cpu_percent",
             "num_threads",
             "name"] # list of metrics to call on psutil.Process object
  pids = list(map(int, get_processes()))
  process_objs = [psutil.Process(pid) for pid in pids]
  
  if args.process_in_parallel:
    pool = Pool(os.cpu_count(), worker_init, [queue])
    all_process_metrics = [process_metrics for process_metrics in pool.map(get_process_metrics, list(zip(process_objs, repeat(metrics, len(process_objs)))))]
    pool.close()
    pool.join()
    queue_listener.stop()
  else:
    all_process_metrics = [get_process_metrics([process_objs, metrics_])
                            for process_objs, metrics_ in list(zip(process_objs, repeat(metrics, len(process_objs))))]
  all_process_metrics = pd.DataFrame(all_process_metrics)
  return all_process_metrics

# end

if __name__ == "__main__":
  all_process_metrics = sys_poll_main()
