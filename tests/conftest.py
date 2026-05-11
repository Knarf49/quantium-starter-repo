import threading
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture(scope="session")
def dash_server():
    from app import app
    thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=8051, debug=False, use_reloader=False),
        daemon=True,
    )
    thread.start()

    import time
    import urllib.request
    for _ in range(20):
        try:
            urllib.request.urlopen("http://127.0.0.1:8051", timeout=1)
            break
        except Exception:
            time.sleep(0.5)
