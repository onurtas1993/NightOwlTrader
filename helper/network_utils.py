import subprocess
import platform


def is_internet_accessible() -> bool:
    """
    Checks internet connectivity by pinging www.google.com.
    Returns True if accessible, False otherwise.
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, "1", "www.google.com"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False
