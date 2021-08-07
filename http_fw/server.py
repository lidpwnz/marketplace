from socketserver import StreamRequestHandler, ThreadingTCPServer
from .request import Request
from .response import Response
from .router import Router
from .static_responder import StaticResponder


def run(router: Router, config: dict) -> None:
    class Handler(StreamRequestHandler):
        def handle(self) -> None:
            request = Request(self.rfile)
            response = Response(self.wfile)
            response.add_header('Connection', 'close')

            static = StaticResponder(request, response, config['static_img'])

            if static.file:
                static.prepare_response()
            else:
                router.run(request, response)

            response.send()

    ThreadingTCPServer.allow_reuse_address = True
    address = (config['host'], config['port'])

    with ThreadingTCPServer(address, Handler) as s:
        s.serve_forever()
