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
