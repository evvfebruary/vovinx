from server.vovingx import Server
from handlers.config import read_config


if __name__ == '__main__':
    server = Server(read_config("/Users/evv/PycharmProjects/vovingx/config/httpd.conf"))
    server.server_init()
