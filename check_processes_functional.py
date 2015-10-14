#!/usr/bin/python3.4
import psutil
import sys


def get_active_processes(process_list):
    active_processes = []
    for process in process_list:
        if process.is_running():
            percent = process.cpu_percent(.2)
            if percent > 0.0:
                active_processes.append({'Name': process.name(), 'PID': process.pid, 'CPU_Percent': percent})

    return active_processes


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

active_processes = get_active_processes(process for process in psutil.process_iter())
printer(active_processes)
exiter(active_processes)

