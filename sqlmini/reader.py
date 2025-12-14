# sqlmini/reader.py
import struct

def read_ccol(ccol_path: str):
    with open(ccol_path, "rb") as f:
        num_cols = struct.unpack("I", f.read(4))[0]
        data = {}
        for _ in range(num_cols):
            name_len = struct.unpack("I", f.read(4))[0]
            col_name = f.read(name_len).decode("utf-8")
            num_vals = struct.unpack("I", f.read(4))[0]
            values = []
            for _ in range(num_vals):
                val_len = struct.unpack("I", f.read(4))[0]
                val = f.read(val_len).decode("utf-8")
                values.append(val)
            data[col_name] = values
        return data
