import subprocess

def run_command(command: list[str], cwd: str | None = None) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False
        )
        success = result.returncode == 0
        return success, result.stdout
    except Exception as e:
        print(f"Error running command {' '.join(command)}: {e}")
        return False, str(e)
