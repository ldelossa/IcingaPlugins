#!/usr/bin/python3.4
import psutil
import sys

processes = [proc for proc in psutil.process_iter()]

process_list = []
for process in processes:
    if process.is_running():
        percent = process.cpu_percent(.2)
        if percent > 0.0:
            process_list.append({'Name': process.name(), 'PID': process.pid,
                                 'CPU_Percent': percent})

for process in process_list:
    print("Name: %s, PID: %s, Percent: %s; " % (process['Name'], process['PID'], process['CPU_Percent']), end="")

print(" | ", end="")

for process in process_list:
    print("%s : %s=%s;;;; " % (process['Name'], process['PID'], process['CPU_Percent']), end="")

if any(percent['CPU_Percent'] > 80.0 and percent['CPU_Percent'] < 90.0 for percent in process_list):
    sys.exit(1)

if any(percent['CPU_Percent'] > 90.0 for percent in process_list):
    sys.exit(2)

