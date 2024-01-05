# Benchmarking Programming Languages

University of Manchester - 3rd Year Project - Benchmarking Programming Languages 

## Brief Description 

This tool is designed for comprehensive performance benchmarking of Python and PyPy scripts. 
It utilizes various metrics such as CPU usage, memory usage, execution time, disk and network usage to provide a thorough analysis of script performance.
This tool is for developers looking to optimize their Python scripts and allows them to capture performance difference between python and PyPy.

## Introduction 

### Purpose 

The benchmarking tool is crucial for identifying performance bottlenecks in Python and PyPy scripts,
enabling developers to understand how code changes impact overall performance across different environments and systems. 

### Features 

- Multi-threading and Multi-processing Support: Facilitates benchmarks under different concurrency models to simulate real-world usage.  
- Profiling: Using cProfiler and snakeviz to see the overall performance of the code and allows users to see the hotspots of the code. Offers in-depth performance analysis of scripts 
- Resource Monitoring: Provides insights into CPU, memory, disk, and network usage during script execution


## Prerequisites 
To effectively use this tool, the followings are required 

- Python: Version 3.0 or later versions
- Operating System: Compatible with Windows, macOS, and Linux
- Dependencies: Requires a download of the requirements.txt file

## Usage 

### Basic Usage 

- Example: 'python comparison.py <interpreter> <script_name> --runs 1 --display --csv --concurrency --snakeviz' to perform a basic benchmark

### Options and Arguments 

interpreter: Select the Python interpreter python3 or pypy.
script_name: Specify the script name for benchmarking.
--runs: Set the number of benchmark iterations.
--display: Toggle the display of results on the console.
--csv: Enable saving results to a CSV file.
--concurrency: Activate multi-threaded and multi-process benchmarks.
--snakeviz: Integrate with snakeviz for profiling visualization.
(if snakeviz is used it will pop up the snakeviz window at the end of the script)



