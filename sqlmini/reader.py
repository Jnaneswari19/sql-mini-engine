# sqlmini/reader.py
import struct

def read_ccol(ccol_path: str, columns: list[str] = None):
    with open(ccol_path, "rb") as f:
        num_cols = struct.unpack("I", f.read(4))[0]
        data = {}
        for _ in range(num_cols):
            name_len = struct.unpack("I", f.read(4))[0]
            col_name = f.read(name_len).decode("utf-8")
            num_vals = struct.unpack("I", f.read(4))[0]

            # If selective read is requested, skip unneeded columns
            if columns and col_name not in columns:
                # Skip values without decoding
                for _ in range(num_vals):
                    val_len = struct.unpack("I", f.read(4))[0]
                    f.seek(val_len, 1)  # jump ahead
                continue

            values = []
            for _ in range(num_vals):
                val_len = struct.unpack("I", f.read(4))[0]
                val = f.read(val_len).decode("utf-8")
                values.append(val)
            data[col_name] = values
        return data
