import sys
import time
import subprocess
import argparse
import pandas as pd
import psutil
import timeit
import gc 
from datetime import datetime
import cProfile
import pstats
from io import StringIO
import numpy as np
from scipy.stats import t
import matplotlib.pyplot as plt
import memray
import tempfile
import concurrent.futures
import platform 
import webbrowser
import os 

class Benchmark:
    def __init__(self, interpreter, script_name, runs=100, display=False, csv=False, snakeviz=False):
        self.interpreter = interpreter
        self.script_name = script_name
        self.runs = runs
        self.display = display
        self.csv = csv
        self.snakeviz = snakeviz
        self.results = [] 

    def log_system_info(self):
        print("System Information:")
        print(f"Operating System: {platform.system()} {platform.release()}")
        print(f"Processor: {platform.processor()}")
        print(f"CPU Count: {psutil.cpu_count(logical=True)}")
        print(f"Total Memory: {psutil.virtual_memory().total / (1024**3):.2f} GB")


    def run_with_threads(self):
        start_time = time.time()
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(subprocess.check_call, [self.interpreter, self.script_name]) for _ in range(self.runs)]
                concurrent.futures.wait(futures)
        except subprocess.CalledProcessError as e:
            print("Error: {}".format(e))
            sys.exit(1)
        end_time = time.time()
        return start_time, end_time - start_time

    # Add a function for multi-process execution
    def run_with_processes(self):
        start_time = time.time()
        try:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                futures = [executor.submit(subprocess.check_call, [self.interpreter, self.script_name]) for _ in range(self.runs)]
                concurrent.futures.wait(futures)
        except subprocess.CalledProcessError as e:
            print("Error: {}".format(e))
            sys.exit(1)
        end_time = time.time()
        return start_time, end_time - start_time

    def run_with_timer(self):
        start_time = time.time()
        try:
            subprocess.check_call([self.interpreter, self.script_name])
        except subprocess.CalledProcessError as e:
            print("Error: {}".format(e))
            sys.exit(1)
        end_time = time.time()
        return start_time, end_time - start_time

    def profile_script(self):
        profile_filename = f"profile_output_{self.interpreter}.prof"
        profile = cProfile.Profile()
        try:
            profile.enable()
            subprocess.check_call([self.interpreter, '-m', 'cProfile', '-o', profile_filename, self.script_name])
        except subprocess.CalledProcessError as e:
            print("Error: {}".format(e))
            sys.exit(1)
        profile.disable()
        print("\nProfiling results:")

        s = StringIO()
        ps = pstats.Stats(profile, stream=s).strip_dirs().sort_stats('cumulative')
        ps.print_stats()
        print(s.getvalue())

        return profile_filename

    def visualize_with_snakeviz(self, profile_filename):
        os.system(f"snakeviz {profile_filename}")

    def resource_usage(self):
        pid = subprocess.Popen([self.interpreter, self.script_name]).pid
        process = psutil.Process(pid)
        
        # Get CPU statistics
        cpu_stats = psutil.cpu_percent(percpu=True)
        total_cpu_percent = sum(cpu_stats) / len(cpu_stats)

        # Get memory statistics
        memory_stats = process.memory_info()

        # Additional stats: Disk and Network
        disk_usage = self.disk_usage()
        network_usage = self.network_usage()

        return {
            'cpu_percent': total_cpu_percent,
            'memory_rss': memory_stats.rss,

            #adding 'disk read-write', network metrics
            'disk_read': disk_usage['read_bytes'],
            'disk_write': disk_usage['write_bytes'],
            'network_sent': network_usage['bytes_sent'],
            'network_received': network_usage['bytes_recv']
        }

    def disk_usage(self):
        disk_io_start = psutil.disk_io_counters()
        # Wait for a short duration to measure disk IO
        time.sleep(4)
        disk_io_end = psutil.disk_io_counters()
        read_bytes = disk_io_end.read_bytes - disk_io_start.read_bytes
        write_bytes = disk_io_end.write_bytes - disk_io_start.write_bytes
        return {'read_bytes': read_bytes, 'write_bytes': write_bytes}

    def network_usage(self):
        net_io_start = psutil.net_io_counters()
        # Wait for a short duration to measure network IO
        time.sleep(4)
        net_io_end = psutil.net_io_counters()
        bytes_sent = net_io_end.bytes_sent - net_io_start.bytes_sent
        bytes_recv = net_io_end.bytes_recv - net_io_start.bytes_recv
        return {'bytes_sent': bytes_sent, 'bytes_recv': bytes_recv}
    

    def run_benchmarks(self):
        print(f"Running benchmarks for {self.interpreter} on {self.script_name}")

        # Profile the script before running benchmarks
        profile_filename = self.profile_script()

        self.log_system_info()

        # Corrected header with placeholders for each column
        header = "{:<10}\t{:<15}\t{:<15}\t{:<15}\t{:<15}\t{:<15}\t{:<15}".format(
        "RUN COUNT", "RUN TYPE", "ELAPSED TIME", "CPU PERCENT", "MEMORY RSS", "DISK USAGE", "NETWORK USAGE")

        print(header)

        for run in range(self.runs):
            # Single-threaded run
            start_time, elapsed_time = self.run_with_timer()
            resource_usage = self.resource_usage()
            result = {
                "elapsed_time": elapsed_time,
                **resource_usage
            }
            self.results.append(result)
            print("{:<10}\t{:<15}\t{:<15.6f}\t{:<15.2f}\t{:<15}\t{:<15}\t{:<15}".format(
            run + 1, "SINGLE-THREADED", elapsed_time, resource_usage['cpu_percent'], 
            resource_usage['memory_rss'], resource_usage['disk_read'] + resource_usage['disk_write'], 
            resource_usage['network_sent'] + resource_usage['network_received'])
            )

        for run in range(self.runs):
            # Multi-threaded run
            start_time, elapsed_time = self.run_with_threads()
            resource_usage = self.resource_usage()
            result = {
                "elapsed_time": elapsed_time,
                **resource_usage
            }
            self.results.append(result)
            print("{:<10}\t{:<15}\t{:<15.6f}\t{:<15.2f}\t{:<15}\t{:<15}\t{:<15}".format(
            run + 1, "MULTI-THREADED", elapsed_time, resource_usage['cpu_percent'], 
            resource_usage['memory_rss'], resource_usage['disk_read'] + resource_usage['disk_write'], 
            resource_usage['network_sent'] + resource_usage['network_received'])
            )

        for run in range(self.runs):
            # Multi-process run
            start_time, elapsed_time = self.run_with_processes()
            resource_usage = self.resource_usage()
            result = {
                "elapsed_time": elapsed_time,
                **resource_usage
            }
            self.results.append(result)
            print("{:<10}\t{:<15}\t{:<15.6f}\t{:<15.2f}\t{:<15}\t{:<15}\t{:<15}".format(
            run + 1, "MULTI-PROCESS", elapsed_time, resource_usage['cpu_percent'], 
            resource_usage['memory_rss'], resource_usage['disk_read'] + resource_usage['disk_write'], 
            resource_usage['network_sent'] + resource_usage['network_received'])
            )

        if self.csv:
            df = pd.DataFrame(self.results)
            df.to_csv(f"benchmark_results_{self.interpreter}_{self.script_name}.csv", index=False)

        single_threaded_results = [result for result in self.results[:self.runs]]
        multi_threaded_results = [result for result in self.results[self.runs:2 * self.runs]]
        multi_process_results = [result for result in self.results[2 * self.runs:]]

        if single_threaded_results:
            avg_single_threaded_time = np.mean([result["elapsed_time"] for result in single_threaded_results])
            avg_single_threaded_cpu_percent = np.mean([result["cpu_percent"] for result in single_threaded_results])
            avg_single_threaded_memory_rss = np.mean([result["memory_rss"] for result in single_threaded_results])
            print(f"\nSingle Thread Run: Average Elapsed Time: {avg_single_threaded_time:.6f} seconds")
            print(f"Average CPU Percent: {avg_single_threaded_cpu_percent:.2f}%")
            print(f"Average Memory RSS: {avg_single_threaded_memory_rss} bytes")

        if multi_threaded_results:
            avg_multi_threaded_time = np.mean([result["elapsed_time"] for result in multi_threaded_results])
            avg_multi_threaded_cpu_percent = np.mean([result["cpu_percent"] for result in multi_threaded_results])
            avg_multi_threaded_memory_rss = np.mean([result["memory_rss"] for result in multi_threaded_results])
            print(f"\nMulti Thread Run: Average Elapsed Time: {avg_multi_threaded_time:.6f} seconds")
            print(f"Average CPU Percent: {avg_multi_threaded_cpu_percent:.2f}%")
            print(f"Average Memory RSS: {avg_multi_threaded_memory_rss} bytes")

        if multi_process_results:
            avg_multi_process_time = np.mean([result["elapsed_time"] for result in multi_process_results])
            avg_multi_process_cpu_percent = np.mean([result["cpu_percent"] for result in multi_process_results])
            avg_multi_process_memory_rss = np.mean([result["memory_rss"] for result in multi_process_results])
            print(f"\nMulti Process Run: Average Elapsed Time: {avg_multi_process_time:.6f} seconds")
            print(f"Average CPU Percent: {avg_multi_process_cpu_percent:.2f}%")
            print(f"Average Memory RSS: {avg_multi_process_memory_rss} bytes")

        if self.snakeviz:
            self.visualize_with_snakeviz(profile_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Benchmark Script")
    parser.add_argument("interpreter", help="Python interpreter to use (e.g., python, pypy)")
    parser.add_argument("script_name", help="Name of the Python script to benchmark")
    parser.add_argument("--runs", type=int, default=100, help="Number of runs for the benchmark")
    parser.add_argument("--display", action="store_true", help="Display benchmark results")
    parser.add_argument("--csv", action="store_true", help="Save benchmark results to CSV file")
    parser.add_argument("--concurrency", action="store_true", help="Run multi-threaded and multi-process benchmarks")
    parser.add_argument("--snakeviz", action="store_true", help="Visualize profiling results with snakeviz")

    args = parser.parse_args()

    # Continue with running benchmarks
    benchmark = Benchmark(args.interpreter, args.script_name, args.runs, args.display, args.csv, args.snakeviz)

    if args.concurrency:
        benchmark.run_benchmarks()
    else: 
        benchmark.run_benchmarks()

    # Allow some time for the results to be printed before exiting
    time.sleep(1)

