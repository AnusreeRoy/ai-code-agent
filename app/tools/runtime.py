import subprocess
import tempfile
import os

def run_python_file(code: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(code.encode())
        path = f.name

    result = subprocess.run(
        ["python", path],
        capture_output=True,
        text=True
    )

    os.unlink(path)

    return result.returncode == 0, result.stdout, result.stderr


def run_java_code(code: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "Main.java")

        with open(file_path, "w") as f:
            f.write(code)

        compile_proc = subprocess.run(
            ["javac", file_path],
            capture_output=True,
            text=True
        )

        if compile_proc.returncode != 0:
            return False, "", compile_proc.stderr

        run_proc = subprocess.run(
            ["java", "-cp", tmpdir, "Main"],
            capture_output=True,
            text=True
        )

        return run_proc.returncode == 0, run_proc.stdout, run_proc.stderr
    
    
def run_javascript_code(code: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as f:
        f.write(code.encode())
        path = f.name

    result = subprocess.run(
        ["node", path],
        capture_output=True,
        text=True
    )

    os.unlink(path)

    return result.returncode == 0, result.stdout, result.stderr

def run_code(code: str, language: str):
    if language == "python":
        return run_python_file(code)

    elif language == "java":
        return run_java_code(code)
    
    elif language == "javascript":
        return run_javascript_code(code)

    else:
        return False, "", f"Unsupported language: {language}"

def run_tests(code: str, tests: str, language: str):
    if not tests or not tests.strip():
        return {
            "success": False,
            "stdout": "",
            "stderr": "No tests provided"
        }
    full_code = f"""
{code}

{tests}
"""

    success, stdout, stderr = run_code(full_code, language)

    return {
        "success": success,
        "stdout": stdout,
        "stderr": stderr
    }

run_tests.needs_code = True