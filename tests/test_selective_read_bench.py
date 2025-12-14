# tests/test_selective_read_bench.py
import time
from sqlmini.writer import write_ccol
from sqlmini.reader import read_ccol
import csv

def benchmark_csv_selective():
    start = time.perf_counter()
    with open("data/people.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        ages = [row["age"] for row in reader]  # only one column
    end = time.perf_counter()
    return end - start

def benchmark_ccol_selective():
    write_ccol("data/people.csv", "data/people.ccol")
    start = time.perf_counter()
    data = read_ccol("data/people.ccol", columns=["age"])  # selective read
    end = time.perf_counter()
    return end - start

def test_compare_selective():
    csv_time = benchmark_csv_selective()
    ccol_time = benchmark_ccol_selective()
    print(f"CSV selective read: {csv_time:.6f}s")
    print(f"CCOL selective read: {ccol_time:.6f}s")
