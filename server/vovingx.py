import socket
from http import HTTPStatus
from handlers.config import *
from handlers import http_handlers
from handlers.logger import logger
from handlers.io_handlers import open_io
from handlers.http_metadata import CONTENT_TYPES, HTTP_VERSION


class Server:

    @staticmethod
    def content_type(filepath):
        return CONTENT_TYPES.get(filepath.split('.')[-1])

    def __init__(self, config):
        self.answers = {
            "FORBIDDEN": http_handlers.response_handler(http_version=HTTP_VERSION,
                                                        status_code=HTTPStatus.FORBIDDEN),
            "NOT_FOUND": http_handlers.response_handler(http_version=HTTP_VERSION,
                                                        status_code=HTTPStatus.NOT_FOUND),
            "NOT_ALLOWED": http_handlers.response_handler(http_version=HTTP_VERSION,
                                                          status_code=HTTPStatus.METHOD_NOT_ALLOWED)
        }
        self.root = config["document_root"]
        self.queue = config["queue"]
        self.forking_workers = []
        self.binding = config["binding"]
        self.size = config["datasize"]
        self.cpu_number = config["cpu_limit"]
        self.socket = None

    def socket_initialize(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(self.binding)
        server_socket.listen(self.queue)
        self.socket = server_socket
        logger.info(f"""Binding on {self.binding} with process count {self.cpu_number} with filepath {self.root}""")

    def file_handler(self, filepath):
        content_type = None
        content_length = 0

        data, error = open_io(filepath)
        if error:
            logger.info(f"Error in reading file with filename:{filepath}")  # Raise some exception?
        else:
            content_length = len(data)
            content_type = self.content_type(filepath)
        return data, content_length, content_type

    def handle_request(self, request):
        filepath = os.path.normpath(self.root + request.path)
        # Prefix check
        if os.path.commonprefix([self.root, filepath]) != self.root:
            return self.answers["FORBIDDEN"]
        if request.method not in ("GET", "HEAD"):
            return self.answers["NOT_ALLOWED"]
        elif not os.path.exists(filepath):
            return self.answers["NOT_FOUND"]

        # Check dir path
        if os.path.isdir(filepath):
            filepath += '/index.html'
        if not os.path.exists(filepath):
            return self.answers["FORBIDDEN"]
        if not os.path.isfile(filepath):
            return self.answers["FORBIDDEN"]

        data, content_length, content_type = self.file_handler(filepath)

        if content_type is None:
            return self.answers["NOT_FOUND"]

        if request.method == 'HEAD':
            return http_handlers.response_handler(http_version=HTTP_VERSION,
                                                  status_code=HTTPStatus.OK,
                                                  content_len=content_length,
                                                  content_type=content_type)

        return http_handlers.response_handler(http_version=HTTP_VERSION,
                                              status_code=HTTPStatus.OK,
                                              content_len=content_length,
                                              content_type=content_type,
                                              data=data)

    def server_init(self):
        self.socket_initialize()
        for worker in range(self.cpu_number):
            pid = os.fork()
            if pid > 0:
                self.forking_workers.append(pid)
            elif pid == 0:
                logger.info(f'Create new worker with pid: {os.getpid()}')
                while True:
                    client_socket, client_address = self.socket.accept()
                    raw_request = client_socket.recv(self.size)
                    if raw_request.strip() == 0:
                        client_socket.close()
                        continue
                    request = http_handlers.request_handler(raw_request)
                    logger.info(request)
                    if not request.validated:
                        response = self.answers["FORBIDDEN"]
                    else:
                        response = self.handle_request(request)
                    client_socket.send(bytes(response))
                    client_socket.close()
            else:
                logger.info("Cant fork anymore")
        self.socket.close()
        for worker_pid in self.forking_workers:
            os.waitpid(worker_pid, 0)


if __name__ == '__main__':
    server = Server(read_config("/etc/httpd.conf"))
    server.server_init()
