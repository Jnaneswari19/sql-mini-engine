# sqlmini/cli.py
from sqlmini.engine import execute
from sqlmini.errors import ParseError

def main():
    print("Welcome to SQL Mini Engine! Type your SQL queries or 'exit' to quit.")
    while True:
        try:
            sql = input("sql> ").strip()
            if not sql:
                continue
            if sql.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            result = execute(sql)
            print(result)
        except ParseError as e:
            print(f"Parse error: {e}")
        except Exception as e:
            print(f"Execution error: {e}")

if __name__ == "__main__":
    main()
