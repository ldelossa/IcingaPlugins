#!/usr/bin/python3.4
import psutil
import sys
import threading
import queue
from multiprocessing.pool import ThreadPool

def get_active_process(process):
    if process.is_running():
        percent = process.cpu_percent(.5)
        if percent > 0.0:
            active_process = {'Name': process.name(), 'PID': process.pid, 'CPU_Percent': percent}
            return active_process


def printer(active_process_list):
    [print("Name: %s, PID: %s, Percent: %s; " % (process['Name'], process['PID'], process['CPU_Percent']), end="") for
        process in active_process_list]

    print(" | ", end="")

    [print("Name: %s Pid: %s=%s;;;; " % (process['Name'], process['PID'], process['CPU_Percent']), end="") for
        process in active_process_list]


def exiter(active_process_list):
    if any(percent['CPU_Percent'] > 80.0 and percent['CPU_Percent'] < 90.0 for percent in active_process_list):
        sys.exit(1)

    elif any(percent['CPU_Percent'] > 90.0 for percent in active_process_list):
        sys.exit(2)

    else:
        sys.exit(0)


processes = (process for process in psutil.process_iter())

pool = ThreadPool(processes=6)
results = [pool.apply_async(get_active_process, args=(x,)) for x in processes]
active_processes = [p.get() for p in results if p.get() is not None]




# q = queue.Queue()
# threads = []
# for process in processes:
#     t = threading.Thread(target=get_active_process, args=(process, q))
#     threads.append(t)
#     t.start()
# print(len(threads))
#
# [t.join() for t in threads]



printer(active_processes)
exiter(active_processes)

