# sqlmini/reader.py
import struct

# Naive CCOL reader (Step 7 + Step 8 selective read)
def read_ccol(ccol_path: str, columns: list[str] = None):
    """
    Read CCOL file in naive format.
    If 'columns' is provided, only those columns are read (selective read).
    """
    with open(ccol_path, "rb") as f:
        num_cols = struct.unpack("I", f.read(4))[0]
        data = {}
        for _ in range(num_cols):
            name_len = struct.unpack("I", f.read(4))[0]
            col_name = f.read(name_len).decode("utf-8")
            num_vals = struct.unpack("I", f.read(4))[0]

            # Skip unneeded columns if selective read
            if columns and col_name not in columns:
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


# Optimized CCOL reader with string offsets (Step 9)
def read_ccol_with_offsets(ccol_path: str):
    """
    Read CCOL file using string pool + offsets.
    """
    with open(ccol_path, "rb") as f:
        num_cols = struct.unpack("I", f.read(4))[0]
        offsets = {}
        for _ in range(num_cols):
            name_len = struct.unpack("I", f.read(4))[0]
            col_name = f.read(name_len).decode("utf-8")
            num_vals = struct.unpack("I", f.read(4))[0]
            idxs = [struct.unpack("I", f.read(4))[0] for _ in range(num_vals)]
            offsets[col_name] = idxs

        # Read string pool
        pool_size = struct.unpack("I", f.read(4))[0]
        pool = []
        for _ in range(pool_size):
            s_len = struct.unpack("I", f.read(4))[0]
            s = f.read(s_len).decode("utf-8")
            pool.append(s)

        # Map offsets back to values
        data = {}
        for col, idxs in offsets.items():
            data[col] = [pool[i] for i in idxs]

        return data
