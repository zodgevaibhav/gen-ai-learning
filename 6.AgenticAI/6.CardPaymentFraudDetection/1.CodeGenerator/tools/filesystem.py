import os
from typing import List

def write_file(file_name: str, data: str, run_dir) -> None:
    file_path = os.path.join(run_dir, file_name)
    
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, "w") as f:
        f.write(data)
    print(f"✓ {file_path}")

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

        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(path, "w") as f:
            f.write(content)

        created_files.append(path)
        print(f"✓ {path}")

    return created_files

# if __name__ == "__main__":
#     file_to_read="/Users/vzodge/Documents/ALL_GITHUB_REPO/gen-ai-learning/6.AgenticAI/6.CardPaymentFraudDetection/1.CodeGenerator/runs/run_20251231_210220/rule_service_code.py"
#     with open(file_to_read, "r") as f:
#         useCaseMarkup = f.read()
#     materialize_files(useCaseMarkup)