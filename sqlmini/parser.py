# sqlmini/parser.py
import re

class ParseError(Exception):
    """Custom error for SQL parsing problems."""
    pass

def parse(sql: str) -> dict:
    """
    Parse a simplified SQL query into components.
    Supported grammar:
      SELECT <* | col[, col...]> | COUNT(*|col)
      FROM <table>
      [WHERE <column> <op> <value>]
    """
    if not sql or not sql.strip():
        raise ParseError("Empty SQL query.")

    # Regex to capture SELECT, FROM, optional WHERE
    m = re.match(
        r"(?is)^\s*SELECT\s+(.*?)\s+FROM\s+([A-Za-z0-9_\-.]+)(?:\s+WHERE\s+(.*))?\s*;?\s*$",
        sql.strip()
    )
    if not m:
        raise ParseError("Invalid SQL. Expected: SELECT ... FROM <table> [WHERE ...]")

    select_part, from_table, where_part = m.group(1), m.group(2), m.group(3)

    # Handle SELECT clause
    select_part = select_part.strip()
    if select_part.upper().startswith("COUNT("):
        arg = select_part[6:-1].strip()
        select_clause = {"aggregate": "COUNT", "arg": arg}
    elif select_part == "*":
        select_clause = {"columns": ["*"]}
    else:
        cols = [c.strip() for c in select_part.split(",") if c.strip()]
        if not cols:
            raise ParseError("SELECT clause must specify columns or COUNT().")
        select_clause = {"columns": cols}

    # Handle WHERE clause
    where_clause = None
    if where_part:
        pattern = r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(=|!=|>=|<=|>|<)\s*(.+?)\s*$"
        m2 = re.match(pattern, where_part.strip())
        if not m2:
            raise ParseError("Invalid WHERE clause syntax.")
        col, op, val_raw = m2.group(1), m2.group(2), m2.group(3).strip()

        # ✅ Fix: remove trailing semicolon if present
        val_raw = val_raw.rstrip(';').strip()

        # Detect quoted string vs number
        if (val_raw.startswith("'") and val_raw.endswith("'")) or (val_raw.startswith('"') and val_raw.endswith('"')):
            value = val_raw[1:-1]
        else:
            try:
                value = int(val_raw)
            except ValueError:
                try:
                    value = float(val_raw)
                except ValueError:
                    value = val_raw

        where_clause = {"col": col, "op": op, "val": value}

    return {
        "select": select_clause,
        "from_table": from_table,
        "where": where_clause
    }
