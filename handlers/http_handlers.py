import datetime
from collections import namedtuple
from urllib.parse import unquote
from handlers.logger import logger

Request = namedtuple("Request", 'body method validated path')


def request_handler(input_request):
    method, path = None, None
    logger.info(f"Input raw request {input_request} \n")
    request_body = input_request.decode('utf-8')
    request_by_string = request_body.split(" ")
    validate = True if len(request_by_string) >= 3 else False  # Minimum length ( head example )
    if validate:
        method = request_by_string[0]
        path = unquote(request_by_string[1].split('?')[0])

    processing_request = Request(input_request.decode('utf-8'),
                                 method,
                                 validate,
                                 path)
    return processing_request


def response_handler(http_version=None, status_code=None,
                     server=None, content_len=None, content_type=None, data=None):
    no_content_response = "\r\n".join([f"{http_version} {int(status_code)} {status_code.name}",
                 f"Server: {server}",
                 f"Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"])
    response_string = no_content_response
    if content_len is not None:
        response_string += f"Content-Length: {content_len}\r\n"
    if content_type is not None:
        response_string += f"Content-Type: {content_type}\r\n"
    response_string += '\r\n'
    response_string = response_string.encode('utf-8')
    if data is not None:
        response_string += data
    return response_string
