# tests/test_engine.py
import pytest
from sqlmini.engine import execute

def test_select_all():
    result = execute("SELECT * FROM people;")
    assert isinstance(result, list)
    assert result[0]["name"] == "Alice"

def test_select_where():
    result = execute("SELECT name, age FROM people WHERE age >= 30;")
    names = [r["name"] for r in result]
    assert "Bob" in names
    assert "Elan" in names
    assert "Alice" not in names

def test_count_star():
    result = execute("SELECT COUNT(*) FROM sales;")
    assert result == 4

def test_count_column():
    result = execute("SELECT COUNT(country) FROM people WHERE age < 40;")
    assert result == 3
