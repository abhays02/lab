"""Open the bundled, offline Lab explorer using the user's default browser."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import threading
from urllib.request import urlopen
import webbrowser


class StaticHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        self.send_error(404, "Directory listing is disabled")
        return None


def site_directory():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "site"
    return Path(__file__).resolve().parents[1] / "dist" / "site"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke-test", action="store_true", help="Check the bundled site, then exit")
    args = parser.parse_args()
    directory = site_directory()
    if not (directory / "index.html").is_file():
        parser.error("Website bundle not found; run scripts/build_site.py first.")
    handler = partial(StaticHandler, directory=str(directory))
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        url = f"http://127.0.0.1:{server.server_port}/"
        if args.smoke_test:
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                with urlopen(url, timeout=10) as response:
                    if response.status != 200 or b"<html" not in response.read().lower():
                        raise RuntimeError("Bundled landing page did not load")
                print("Offline explorer smoke test passed.")
            finally:
                server.shutdown()
                worker.join()
            return
        print(f"Lab explorer: {url}\nKeep this window open. Press Ctrl+C to close the server.")
        if not webbrowser.open(url):
            print("Open the address above in your browser.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nLab explorer closed.")


if __name__ == "__main__":
    main()
