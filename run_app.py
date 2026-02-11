import argparse
import os
import subprocess
import sys
import time
import webbrowser


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Streamlit app and open browser.")
    parser.add_argument("--port", type=int, default=8501, help="Port to bind Streamlit server.")
    parser.add_argument("--address", default="localhost", help="Server address to open.")
    args = parser.parse_args()

    url = f"http://{args.address}:{args.port}"

    # التأكد من تشغيل التطبيق من المجلد الصحيح
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app.py")

    # Start Streamlit server.
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            app_path,
            "--server.port",
            str(args.port),
            "--server.address",
            args.address,
        ]
    )

    # Give the server a moment to start before opening the browser.
    time.sleep(1.5)
    webbrowser.open(url)

    return process.wait()


if __name__ == "__main__":
    raise SystemExit(main())
