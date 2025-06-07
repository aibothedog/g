import http.server
import socketserver
import os
from urllib.parse import unquote
import cgi

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_type = self.headers['Content-Type']
        if not content_type.startswith('multipart/form-data'):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request")
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                filename = os.path.basename(field_item.filename)
                with open(filename, 'wb') as f:
                    f.write(field_item.file.read())

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Upload successful")

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"""
            <html><body>
            <h1>Upload File</h1>
            <form enctype="multipart/form-data" method="post">
              <input name="file" type="file"/>
              <input type="submit" value="Upload"/>
            </form>
            </body></html>
            """)
        else:
            super().do_GET()

PORT = 8080
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
