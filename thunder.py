import tornado.ioloop
import tornado.web
import inspect
from collections import defaultdict
import re

# TODO
# - Authentication

app = []
env = tornado.web.Application()

def handler(methods):
    '''
    Returns a tornado handler with get method defined by the function passed
    via the get decorator
    '''
    class Handler(tornado.web.RequestHandler):
        if 'get' in methods.keys():
            def get(self, *args, **kwargs):
                if len(inspect.getargspec(methods['get']).args) > 0 and \
                        inspect.getargspec(methods['get']).args[0] == 'request':
                    args = (self.request, ) + args
                self.write(methods['get'](*args, **kwargs))
        if 'post' in methods.keys():
            def post(self, *args, **kwargs):
                if len(inspect.getargspec(methods['post']).args) > 0 and \
                        inspect.getargspec(methods['post']).args[0] == 'request':
                    args = (self.request, ) + args
                self.write(methods['post'](*args, **kwargs))
        if 'put' in methods.keys():
            def put(self, *args, **kwargs):
                if len(inspect.getargspec(methods['put']).args) > 0 and \
                        inspect.getargspec(methods['put']).args[0] == 'request':
                    args = (self.request, ) + args
                self.write(methods['put'](*args, **kwargs))
        if 'patch' in methods.keys():
            def patch(self, *args, **kwargs):
                if len(inspect.getargspec(methods['patch']).args) > 0 and \
                        inspect.getargspec(methods['patch']).args[0] == 'request':
                    args = (self.request, ) + args
                self.write(methods['patch'](*args, **kwargs))
    return Handler


# Decorators
def get(path='/'):
    '''
    Adds a function and optional path to the global app variable
    '''
    def _get(func_to_decorate):
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
    # if there is a variable to be substituted, do so recursively
    while re.match(re.compile(r'(.*){[0-9]*}(.*)'), string) or \
            re.match(re.compile(r'(.*){.*}(.*)'), string):
        if re.match(re.compile(r'(.*){[0-9]*}(.*)'), string):
            return args(re.sub(re.compile(r'(.*){[0-9]*}(.*)'),
                               r'\1([^\/]+)\2', string))
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
    #import pdb; pdb.set_trace()
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
    @get('/test/{name}/')
    def named(request, name):
        return name
    @get('/other/{0}/')
    def named(request, name):
        return name
    run()
