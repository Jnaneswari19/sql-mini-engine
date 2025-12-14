# tests/test_offsets_bench.py
import time
from sqlmini.writer import write_ccol_with_offsets
from sqlmini.reader import read_ccol_with_offsets
from sqlmini.writer import write_ccol
from sqlmini.reader import read_ccol

def test_compare_offsets():
    # Naive CCOL
    write_ccol("data/people.csv", "data/people_naive.ccol")
    start = time.perf_counter()
    naive = read_ccol("data/people_naive.ccol")
    naive_time = time.perf_counter() - start

    # Offset CCOL
    write_ccol_with_offsets("data/people.csv", "data/people_offsets.ccol")
    start = time.perf_counter()
    optimized = read_ccol_with_offsets("data/people_offsets.ccol")
    offset_time = time.perf_counter() - start

    print(f"Naive CCOL read: {naive_time:.6f}s")
    print(f"Offset CCOL read: {offset_time:.6f}s")
    assert naive == optimized
