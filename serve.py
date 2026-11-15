#!/usr/bin/env python3
"""Static server for freej2me-web with HTTP Range support.

CheerpJ requires the server to honour Range requests, which Python's
built-in SimpleHTTPRequestHandler does not implement. Run:

    python serve.py [port]

Then open http://localhost:8000/play.html
"""

import mimetypes
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

mimetypes.add_type("application/wasm", ".wasm")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("application/java-archive", ".jar")

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)


class RangeReader:
    """File wrapper that stops after `remaining` bytes."""

    def __init__(self, f, remaining):
        self.f = f
        self.remaining = remaining

    def read(self, n=-1):
        if self.remaining <= 0:
            return b""
        if n is None or n < 0 or n > self.remaining:
            n = self.remaining
        data = self.f.read(n)
        self.remaining -= len(data)
        return data

    def close(self):
        self.f.close()


class Handler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path) or not os.path.isfile(path):
            return super().send_head()

        header = self.headers.get("Range")
        if not header:
            return super().send_head()

        m = re.match(r"bytes=(\d*)-(\d*)$", header.strip())
        if not m:
            return super().send_head()

        size = os.path.getsize(path)
        first, last = m.groups()
        if first == "":
            if last == "":
                return super().send_head()
            length = int(last)
            start = max(0, size - length)
            end = size - 1
        else:
            start = int(first)
            end = int(last) if last else size - 1
            end = min(end, size - 1)

        if start >= size or start > end:
            self.send_error(416, "Requested Range Not Satisfiable")
            return None

        f = open(path, "rb")
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        return RangeReader(f, end - start + 1)

    def log_message(self, fmt, *args):
        # Keep the console quiet about normal requests.
        if args and str(args[1]).startswith(("2", "3")):
            return
        super().log_message(fmt, *args)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print("Serving:", ROOT.encode("ascii", "replace").decode("ascii"))
    print("Open http://localhost:%d/play.html" % port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
