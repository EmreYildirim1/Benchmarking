import sys
import time
import subprocess
import argparse
import pandas as pd
import psutil
import timeit
from datetime import datetime
#from pybench import PyBenchSuite
from microbench import MicroBench, MBPythonVersion, MBHostInfo, MBHostRamTotal

class Benchmark(MicroBench, MBPythonVersion, MBHostInfo, MBHostRamTotal):
    pass

def run_with_timer(interpreter, script_name):
    start_time = time.time()
    try:
        subprocess.check_call([interpreter, script_name])
    except subprocess.CalledProcessError as e:
        print("Error: {}".format(e))
        sys.exit(1)
    end_time = time.time()
    return start_time, end_time - start_time

#def run_pybench_suite(interpreter, suite):
#    result = subprocess.run([interpreter, suite], capture_output=True, text=True)
#    return result.stdout

@Benchmark(outfile='microbench_output.json')
def main():
    parser = argparse.ArgumentParser(description="Comparing time in PyPy and CPython.")
    parser.add_argument("script_name", help="Name of the script to run with PyPy and CPython")
    args = parser.parse_args()

    script_name = args.script_name

    # Running the scripts with PyPy and cpython 
    pypyStartTime, pypy_time = run_with_timer("pypy", script_name)
    cpythonStartTime, cpython_time = run_with_timer("python", script_name)

    pypy_elapsed_time = pypy_time
    cpython_elapsed_time = cpython_time

    # Assuming there is a function or class in pybench that you can use
#    benchmark_results = pybench.run_pybench_suite()

    # Extract and process Pybench results (this depends on the output format of Pybench)
    # You may need to customize this part based on the actual output format
    #pypy_elapsed_time = process_pybench_output(pypy_pybench_output)
    #cpython_elapsed_time = process_pybench_output(cpython_pybench_output)


    #printing the basics in terminal
    print("PyPy Time: {:.4f} seconds".format(pypy_time))
    print("CPython Time: {:.4f} seconds".format(cpython_time))

    #trying to get ram usage for pypy and cpython
    #not effective
    pypy_ram_usage = psutil.Process(subprocess.Popen(['pypy', script_name]).pid).memory_info().rss
    cpython_ram_usage = psutil.Process(subprocess.Popen(['python', script_name]).pid).memory_info().rss

    result_data = {
    	"Start Time PyPy": pypyStartTime,
        "End Time PyPy": pypyStartTime + pypy_time,
        "Start Time CPython": cpythonStartTime,
        "End Time CPython": cpythonStartTime + cpython_time,
        "PyPy": pypy_elapsed_time,
        "Python": cpython_elapsed_time,
        "PyPy RAM Usage": (pypy_ram_usage),
        "CPython RAM Usage": (cpython_ram_usage),
    }

    with open('microbench_output.csv', 'a') as csv_file:
        csv_file.write(f'Start Time PyPy: {pypyStartTime}, End Time PyPy: {pypyStartTime + pypy_time}, '
                       f'Start Time CPython: {cpythonStartTime}, End Time CPython: {cpythonStartTime + cpython_time}, '
                       f'PyPy: {pypy_elapsed_time} seconds, Python: {cpython_elapsed_time} seconds, '
                       f'PyPy RAM Usage: {pypy_ram_usage} bytes, CPython RAM Usage: {cpython_ram_usage} bytes\n')


if __name__ == "__main__":
    main()

print("Results saved to microbench_output.csv.")
