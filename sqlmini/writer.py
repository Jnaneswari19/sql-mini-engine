# sqlmini/writer.py
import csv
import struct

def write_ccol(csv_path: str, ccol_path: str):
    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        data = {col: [] for col in columns}
        for row in reader:
            for col in columns:
                data[col].append(row[col])

    with open(ccol_path, "wb") as out:
        # Write header: number of columns
        out.write(struct.pack("I", len(columns)))
        for col in columns:
            encoded = col.encode("utf-8")
            out.write(struct.pack("I", len(encoded)))
            out.write(encoded)
            # Write column values
            out.write(struct.pack("I", len(data[col])))
            for val in data[col]:
                val_bytes = val.encode("utf-8")
                out.write(struct.pack("I", len(val_bytes)))
                out.write(val_bytes)
