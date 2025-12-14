# tests/test_performance.py
import time
from sqlmini.engine import execute

def benchmark(query: str, repeat: int = 100):
    start = time.perf_counter()
    for _ in range(repeat):
        execute(query)
    end = time.perf_counter()
    return end - start

def test_benchmarks():
    queries = [
        "SELECT * FROM people;",
        "SELECT name, age FROM people WHERE age >= 30;",
        "SELECT COUNT(*) FROM sales;",
        "SELECT COUNT(country) FROM people WHERE age < 40;"
    ]
    for q in queries:
        duration = benchmark(q, repeat=100)
        print(f"{q} -> {duration:.4f} seconds (100 runs)")
