import os
import sys
import threading
import webbrowser
import time

def open_browser(port):
    time.sleep(3)
    webbrowser.open(f"http://localhost:{port}")

def main():
    # PyInstaller set sys._MEIPASS
    if getattr(sys, 'frozen', False):
        app_dir = sys._MEIPASS
    else:
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(app_dir)
    port = "8501"

    # Streamlit CLI module setup
    try:
        from streamlit.web import cli
    except ImportError:
        from streamlit import cli

    sys.argv = [
        "streamlit",
        "run",
        "main.py",
        "--server.port",
        port,
        "--server.headless",
        "true",
        "--global.developmentMode",
        "false"
    ]

    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    sys.exit(cli.main())

if __name__ == "__main__":
    main()
