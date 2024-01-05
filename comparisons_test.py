import pytest
from comparison import Benchmark
import subprocess

# Mock script name for testing
TEST_SCRIPT = "dummy.py"

# Mock class for subprocess calls
class MockSubprocess:
    def check_call(self, command):
        assert isinstance(command, list)
        # Simulate a subprocess call without actually executing a script
        return 0

# Test fixture for the Benchmark class
@pytest.fixture
def benchmark():
    return Benchmark("python", TEST_SCRIPT, runs=5)

# Test logging system information
def test_log_system_info(benchmark):
    benchmark.log_system_info()
    # This function doesn't return anything, but you should manually check the output

# Test run_with_timer method
def test_run_with_timer(monkeypatch, benchmark):
    # Mock subprocess.check_call
    monkeypatch.setattr(subprocess, 'check_call', MockSubprocess().check_call)
    start_time, elapsed_time = benchmark.run_with_timer()
    assert elapsed_time >= 0

# Test run_with_threads method
def test_run_with_threads(monkeypatch, benchmark):
    monkeypatch.setattr(subprocess, 'check_call', MockSubprocess().check_call)
    start_time, elapsed_time = benchmark.run_with_threads()
    assert elapsed_time >= 0

# Test run_with_processes method
def test_run_with_processes(monkeypatch, benchmark):
    monkeypatch.setattr(subprocess, 'check_call', MockSubprocess().check_call)
    start_time, elapsed_time = benchmark.run_with_processes()
    assert elapsed_time >= 0

# Test resource_usage method
def test_resource_usage(benchmark):
    resource_usage = benchmark.resource_usage()
    assert 'cpu_percent' in resource_usage
    assert 'memory_rss' in resource_usage
    assert 'disk_read' in resource_usage
    assert 'disk_write' in resource_usage
    assert 'network_sent' in resource_usage
    assert 'network_received' in resource_usage

# Test disk_usage method
def test_disk_usage(benchmark):
    disk_usage = benchmark.disk_usage()
    assert 'read_bytes' in disk_usage
    assert 'write_bytes' in disk_usage

# Test network_usage method
def test_network_usage(benchmark):
    network_usage = benchmark.network_usage()
    assert 'bytes_sent' in network_usage
    assert 'bytes_recv' in network_usage

# Test profiling
def test_profile_script(monkeypatch, benchmark):
    # Mock subprocess.check_call
    monkeypatch.setattr(subprocess, 'check_call', MockSubprocess().check_call)
    benchmark.profile_script()
    # Check the profiling output manually

# Test the complete benchmark run
def test_run_benchmarks(monkeypatch, benchmark):
    # Mock subprocess.check_call
    monkeypatch.setattr(subprocess, 'check_call', MockSubprocess().check_call)
    benchmark.run_benchmarks()
    # This test doesn't assert anything, but you should manually check the output
