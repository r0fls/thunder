import tornado.ioloop
import tornado.web
import inspect
from collections import defaultdict
import re

# TODO
# - Authentication

app = []
env = tornado.web.Application([],cookie_secret="someshit")

# should add the other dict methods
# these 3 classes should all point
# to the same handler
class Cookies(dict):
    def __init__(self, handler):
        self.handler = handler
        # may not need this
        self.dict = dict()

    def __setitem__(self, key, value):
        self.handler.set_cookie(key, value)
        self.dict[key] = value

    def __getitem__(self, key):
        return self.dict[key]


class Headers(dict):
    def __init__(self, handler):
        self.handler = handler
        self.dict = dict()

    def __setitem__(self, key, value):
        self.handler.set_header(key, value)
        self.dict[key] = value

    def __getitem__(self, key):
        return self.dict[key]


class Response:
    def __init__(self, handler):
        self.handler = handler
        self.headers = Headers(handler)
        self.cookies = Cookies(handler)

def handler(methods):
    '''
    Returns a tornado handler with get method defined by the function passed
    via the get decorator
    '''
    class Handler(tornado.web.RequestHandler):
        if 'get' in methods.keys():
            def get(self, *args, **kwargs):
                func_args = inspect.getargspec(methods['get']).args
                req_index = func_args.index("request") if "request" in func_args else -1
                res_index = func_args.index("response") if "response" in func_args else -1
                if res_index > -1:
                    args = args[:res_index] + (Response(self), ) + args[res_index:]
                    if req_index > -1:
                        args = args[:req_index] + (self.request, ) + args[req_index:]
                elif req_index > -1:
                    args = args[:req_index] + (self.request, ) + args[req_index:]
                self.write(methods['get'](*args, **kwargs))
        if 'post' in methods.keys():
            def post(self, *args, **kwargs):
                func_args = inspect.getargspec(methods['post']).args
                req_index = func_args.index("request") if "request" in func_args else -1
                res_index = func_args.index("response") if "response" in func_args else -1
                if res_index > -1:
                    args = args[:res_index] + (self, ) + args[res_index:]
                    if req_index > -1:
                        args = args[:req_index] + (self.request, ) + args[req_index:]
                elif req_index > -1:
                    args = args[:req_index] + (self.request, ) + args[req_index:]
                self.write(methods['post'](*args, **kwargs))
        if 'put' in methods.keys():
            def put(self, *args, **kwargs):
                func_args = inspect.getargspec(methods['put']).args
                req_index = func_args.index("request") if "request" in func_args else -1
                res_index = func_args.index("response") if "response" in func_args else -1
                if res_index > -1:
                    args = args[:res_index] + (self, ) + args[res_index:]
                    if req_index > -1:
                        args = args[:req_index] + (self.request, ) + args[req_index:]
                elif req_index > -1:
                    args = args[:req_index] + (self.request, ) + args[req_index:]
                self.write(methods['put'](*args, **kwargs))
        if 'patch' in methods.keys():
            def patch(self, *args, **kwargs):
                func_args = inspect.getargspec(methods['patch']).args
                req_index = func_args.index("request") if "request" in func_args else -1
                res_index = func_args.index("response") if "response" in func_args else -1
                if res_index > -1:
                    args = args[:res_index] + (self, ) + args[res_index:]
                    if req_index > -1:
                        args = args[:req_index] + (self.request, ) + args[req_index:]
                elif req_index > -1:
                    args = args[:req_index] + (self.request, ) + args[req_index:]
                self.write(methods['patch'](*args, **kwargs))
    return Handler


# Decorators
def get(path='/'):
    '''
    Adds a function and optional path to the global app variable
    '''
    def _get(func_to_decorate):
        # these two lines aren't doing anything, could allow
        # the get mathod to take more arguments (e.g. auth functions)
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        app.append([r".*", [path, 'get', func_to_decorate]])
    return _get

def post(path='/'):
    '''
    Adds a function and optional path to the global app variable
    '''
    def _post(func_to_decorate):
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        app.append([r".*", [path, 'post', func_to_decorate]])
    return _post

def put(path='/'):
    '''
    Adds a function and optional path to the global app variable
    '''
    def _put(func_to_decorate):
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        app.append([r".*", [path, 'put', func_to_decorate]])
    return _put

def patch(path='/'):
    '''
    Adds a function and optional path to the global app variable
    '''
    def _patch(func_to_decorate):
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        app.append([r".*", [path, 'patch', func_to_decorate]])
    return _patch

def args(string):
    """
    Transforms a route from {} to regex
    """
    # if there is a variable to be substituted, do so recursively
    while re.match(re.compile(r'(.*){[0-9]*}(.*)'), string) or \
            re.match(re.compile(r'(.*){.*}(.*)'), string):
        # indexed parameters
        if re.match(re.compile(r'(.*){[0-9]*}(.*)'), string):
            return args(re.sub(re.compile(r'(.*){[0-9]*}(.*)'),
                               r'\1([^\/]+)\2', string))
        # named parameters
        elif re.match(re.compile(r'(.*){.*}(.*)'), string):
            return args(re.sub(re.compile(r'(.*){(.*)}(.*)'),
                               r'\1(?P<\2>[^\/]+)\3', string))
        else:
            return string
    # there was no match, just resturn the string
    if string[-1] == '/':
        return '{}*'.format(string)
    return '{}/*'.format(string)

def make_app():
    apps = defaultdict(dict)
    for key, value in app:
        if value[0] in apps[key].keys():
            apps[key][value[0]].append(value[1:])
        else:
            apps[key][value[0]] = [value[1:]]
    for key in apps.keys():
        for path in apps[key]:
            try:

                env.add_handlers(key, [(args(path),
                                        handler(dict(apps[key][path])))])
            except Exception as e:
                 s = ("there was a problem adding {0} "
                        "{1} {2}\n {3}")
                 print(s.format(key, path, apps[key][path], e))
    return env

def start(port=8888):
    make_app()
    env.listen(port)
    tornado.ioloop.IOLoop.current().start()

def stop():
    tornado.ioloop.IOLoop.instance().stop()

START ="""\
 _____ _                     _             ____       _ _
|_   _| |__  _   _ _ __   __| | ___ _ __  |  _ \ ___ | | |___
  | | | '_ \| | | | '_ \ / _` |/ _ \ '__| | |_) / _ \| | / __|
  | | | | | | | |_| | | | | (_| | _/ |    |  _ < (_) | | \__ \\
  |_| |_| |_|\__,_|_| |_|\__,_|\___|_|    |_| \_\___/|_|_|___/
"""

def run(port=8888):
    import signal
    import sys

    def signal_handler(signal, frame):
        print('\nStopping Thunder')
        stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print('{0}\nThunder is running on port {1}...\nPress Ctrl+C to exit'.format(START, port))
    start(port)
    signal.pause()

if __name__ == "__main__":
    run()
