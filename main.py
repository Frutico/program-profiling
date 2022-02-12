# -*- coding: utf-8 -*-
#
# 1. The psutil library was used to solve this problem. This library serves as a beautiful wrapper for the two standard libraries - subprocess and os.
# 2. To determine the CPU load, the Windows-like approach was used, when the spent processor time is divided among all logical CPUs in the system. This gives the average result of the CPU.
# 3. After each line of writing data, the file is closed, which is not very optimal, but this will save data in case of OS crashes or power outages
# 4. The log file is saved next to the script. It is possible to specify a directory to save as a parameter.
# 5. A new file is created for each profiling and contains the current date and time in the name
# 6. For convenient storage and automatic generation of graphs, the CSV format with the divisor ";" was chosen.
#
#
# It takes two parameters:
# 1. Source directory
# 2. Interval in seconds

import psutil
import datetime


def get_cpu_usage(process, interval=None):
    return process.cpu_percent(interval=interval) / psutil.cpu_count()


def get_mem_rss_usage(process):
    return process.memory_info().rss


def get_mem_private_usage(process):
    return process.memory_info().private


def get_handle_count(process):
    return len(process.open_files())


def write_log(file_name, gpuUsage, memWS, memPrivate, handles):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d;%H:%M:%S')
    with open(file_name, "a", encoding='utf-8') as f:
        f.write("\n")
        f.write(f"'{current_time}';'{gpuUsage}';'{memWS}';'{memPrivate}';'{handles}'")


def init_log_file(path =""):
    file_name = f"{path}log {datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.csv"
    with open(file_name, "x", encoding='utf-8') as f:
        f.write("date;time;cpu_usage;mem_wm;mem_privacy;handles")
    return file_name


def main():
    path = input("Enter path to file: ")
    interval = float(input("Enter interval (second): "))
    process = psutil.Popen([path])

    file_name = init_log_file()

    while psutil.pid_exists(process.pid):
        try:
            write_log(file_name,
                      get_cpu_usage(process, interval),
                      get_mem_rss_usage(process),
                      get_mem_private_usage(process),
                      get_handle_count(process)
                      )
        except psutil.NoSuchProcess:
            pass

    print("done")

if __name__ == '__main__':
    main()