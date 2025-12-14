# tests/test_parser.py
import pytest
from sqlmini.parser import parse

def test_select_columns():
    sql = "SELECT name, age FROM people WHERE age >= 30;"
    result = parse(sql)
    assert result == {
        "select": {"columns": ["name", "age"]},
        "from_table": "people",
        "where": {"col": "age", "op": ">=", "val": 30}
    }

def test_count_star():
    sql = "SELECT COUNT(*) FROM sales;"
    result = parse(sql)
    assert result == {
        "select": {"aggregate": "COUNT", "arg": "*"},
        "from_table": "sales",
        "where": None
    }

def test_count_column():
    sql = "SELECT COUNT(country) FROM people WHERE age < 40;"
    result = parse(sql)
    assert result == {
        "select": {"aggregate": "COUNT", "arg": "country"},
        "from_table": "people",
        "where": {"col": "age", "op": "<", "val": 40}
    }
