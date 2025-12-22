import os
from typing import List

def materialize_files(output: str) -> List[str]:
    created_files = []

    blocks = output.split("===FILE===")
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.splitlines()
        if len(lines) < 2:
            continue  # malformed block, skip safely

        path = lines[0].strip()
        content = "\n".join(lines[1:])

        dir_path = os.path.dirname(path)

        # ✅ FIX: create dir only if path is non-empty
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(path, "w") as f:
            f.write(content)

        created_files.append(path)
        print(f"✓ {path}")

    return created_files
