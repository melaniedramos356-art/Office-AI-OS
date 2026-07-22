import subprocess
import sys
from pathlib import Path
import os


class SafePythonRunner:
    def __init__(self, temp_folder="outputs/temp_scripts"):
        self.temp_folder = Path(temp_folder)

    def run_code(self, code, script_name="safe_script.py", timeout_seconds=60):
        if not isinstance(code, str) or not code.strip():
            return self.build_result(False, "", "没有收到有效 Python 代码。", "")

        self.temp_folder.mkdir(parents=True, exist_ok=True)
        script_path = self.temp_folder / script_name
        script_path.write_text(code, encoding="utf-8")

        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"
            completed = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            return self.build_result(False, "", "Python 脚本执行超时。", str(script_path))
        except OSError as error:
            return self.build_result(False, "", f"Python 脚本执行失败：{error}", str(script_path))

        return self.build_result(
            completed.returncode == 0,
            completed.stdout,
            completed.stderr,
            str(script_path),
        )

    def build_result(self, success, stdout, stderr, script_path):
        return {
            "success": success,
            "stdout": stdout,
            "stderr": stderr,
            "script_path": script_path,
        }
