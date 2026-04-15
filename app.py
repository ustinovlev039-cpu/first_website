from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

HOST = "127.0.0.1"
PORT = 8080


class MyHandler(BaseHTTPRequestHandler):
    def _send_html_file(self, file_path: str) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h1>404 Not Found</h1>".encode("utf-8"))

    def do_GET(self):
        self._send_html_file("templates/contacts.html")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = parse_qs(post_data)

        print("Получены данные от пользователя:")
        for key, value in parsed_data.items():
            print(f"{key}: {value[0]}")

        self._send_html_file("templates/contacts.html")


def main():
    server = HTTPServer((HOST, PORT), MyHandler)
    print(f"Сервер запущен: http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()