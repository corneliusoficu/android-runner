import http.server
import socketserver

def serve_webpages(port):
    handler = http.server.SimpleHTTPRequestHandler
    server = socketserver.TCPServer(("0.0.0.0", port), handler)
    print("Starting server at port %d" % port)
    server.serve_forever()

if __name__ == '__main__':
    serve_webpages(9191)