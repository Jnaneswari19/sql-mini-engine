# sqlmini/writer.py
import csv
import struct

# Naive CCOL writer (already used in Step 7)
def write_ccol(csv_path: str, ccol_path: str):
    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        data = {col: [] for col in columns}
        for row in reader:
            for col in columns:
                data[col].append(row[col])

    with open(ccol_path, "wb") as out:
        out.write(struct.pack("I", len(columns)))
        for col in columns:
            encoded = col.encode("utf-8")
            out.write(struct.pack("I", len(encoded)))
            out.write(encoded)
            out.write(struct.pack("I", len(data[col])))
            for val in data[col]:
                val_bytes = val.encode("utf-8")
                out.write(struct.pack("I", len(val_bytes)))
                out.write(val_bytes)

# Optimized CCOL writer with string offsets (Step 9)
def write_ccol_with_offsets(csv_path: str, ccol_path: str):
    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        data = {col: [] for col in columns}
        pool = {}
        pool_list = []
        for row in reader:
            for col in columns:
                val = row[col]
                if val not in pool:
                    pool[val] = len(pool_list)
                    pool_list.append(val)
                data[col].append(pool[val])

    with open(ccol_path, "wb") as out:
        out.write(struct.pack("I", len(columns)))
        for col in columns:
            encoded = col.encode("utf-8")
            out.write(struct.pack("I", len(encoded)))
            out.write(encoded)
            out.write(struct.pack("I", len(data[col])))
            for idx in data[col]:
                out.write(struct.pack("I", idx))

        # Write string pool
        out.write(struct.pack("I", len(pool_list)))
        for s in pool_list:
            s_bytes = s.encode("utf-8")
            out.write(struct.pack("I", len(s_bytes)))
            out.write(s_bytes)
