# sqlmini/engine.py
import csv
from sqlmini.parser import parse
from sqlmini.errors import ParseError

def load_table(table_name: str) -> list[dict]:
    """
    Load a CSV file from the data/ folder into a list of dicts.
    """
    path = f"data/{table_name}.csv"
    try:
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        raise ParseError(f"Table '{table_name}' not found at {path}")

def evaluate_where(row: dict, where: dict) -> bool:
    """
    Evaluate a WHERE condition on a single row.
    """
    if not where:
        return True
    col, op, val = where["col"], where["op"], where["val"]
    if col not in row:
        return False
    cell = row[col]

    # Try to convert both cell and val to numbers
    def to_number(x):
        try:
            return int(x)
        except (ValueError, TypeError):
            try:
                return float(x)
            except (ValueError, TypeError):
                return x

    cell_val = to_number(cell)
    val = to_number(val)

    # Handle empty strings gracefully
    if cell_val == "":
        return False

    if op == "=": return cell_val == val
    if op == "!=": return cell_val != val
    if op == ">": return cell_val > val
    if op == "<": return cell_val < val
    if op == ">=": return cell_val >= val
    if op == "<=": return cell_val <= val
    return False

def execute(sql: str):
    """
    Execute a SQL query string against CSV data.
    """
    query = parse(sql)
    rows = load_table(query["from_table"])

    # Apply WHERE filter
    filtered = [r for r in rows if evaluate_where(r, query["where"])]

    # Handle COUNT
    if "aggregate" in query["select"]:
        arg = query["select"]["arg"]
        if arg == "*" or arg not in rows[0]:
            return len(filtered)
        else:
            return sum(1 for r in filtered if r[arg])
    
    # Handle SELECT columns
    cols = query["select"]["columns"]
    if cols == ["*"]:
        return filtered
    else:
        return [{c: r[c] for c in cols if c in r} for r in filtered]
