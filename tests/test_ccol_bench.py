# tests/test_ccol_bench.py
import time
from sqlmini.writer import write_ccol
from sqlmini.reader import read_ccol

def benchmark_csv():
    import csv
    start = time.perf_counter()
    with open("data/people.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    end = time.perf_counter()
    return end - start

def benchmark_ccol():
    write_ccol("data/people.csv", "data/people.ccol")
    start = time.perf_counter()
    data = read_ccol("data/people.ccol")
    end = time.perf_counter()
    return end - start

def test_compare():
    csv_time = benchmark_csv()
    ccol_time = benchmark_ccol()
    print(f"CSV load: {csv_time:.6f}s")
    print(f"CCOL load: {ccol_time:.6f}s")
