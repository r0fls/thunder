import tornado.ioloop
import tornado.web
import inspect
from collections import defaultdict

app = []
env = tornado.web.Application()

def handler(methods):
    '''
    Returns a tornado handler with get method defined by the function passed
    via the get decorator
    '''
    class Handler(tornado.web.RequestHandler):
        if 'get' in methods.keys():
            def get(self):
                if len(inspect.getargspec(methods['get']).args) == 0:
                    self.write(methods['get'])
                elif len(inspect.getargspec(methods['get']).args) == 1:
                    self.write(methods['get'](self.request))
        if 'post' in methods.keys():
            def post(self):
                if len(inspect.getargspec(methods['post']).args) == 0:
                    self.write(methods['post'])
                elif len(inspect.getargspec(methods['post']).args) == 1:
                    self.write(methods['post'](self.request))
        if 'put' in methods.keys():
            def put(self):
                if len(inspect.getargspec(methods['put']).args) == 0:
                    self.write(methods['put'])
                elif len(inspect.getargspec(methods['put']).args) == 1:
                    self.write(methods['put'](self.request))
    return Handler


# Decorators
def get(path='/'):
    '''
    Adds a function and optional path to global env instance
    '''
    # this should match against existing env and append to existing ones
    def _get(func_to_decorate):
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        #env.add_handlers(r".*", [(path, get_handler(func_to_decorate))])
        app.append([r".*", [path, 'get', func_to_decorate]])
    return _get

def post(path='/'):
    '''
    Adds a function and optional path to global env instance
    '''
    # this should match against existing env and append to existing ones
    def _post(func_to_decorate):
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        #env.add_handlers(r".*", [(path, get_handler(func_to_decorate))])
        app.append([r".*", [path, 'post', func_to_decorate]])
    return _post

def put(path='/'):
    '''
    Adds a function and optional path to global env instance
    '''
    # this should match against existing env and append to existing ones
    def _put(func_to_decorate):
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        #env.add_handlers(r".*", [(path, get_handler(func_to_decorate))])
        app.append([r".*", [path, 'put', func_to_decorate]])
    return _put


# move to test
@post('/test')
def headers(request):
    '''echo back the headers'''
    return str(request.body)

# move to test
@get('/test')
def headers(request):
    '''echo back the headers'''
    return str(request.headers)

# move to test
@put('/test')
def headers(request):
    '''echo back the headers'''
    return str(request.body)

def start(port=8888):
    apps = defaultdict(dict)
    for key, value in app:
        if value[0] in apps[key].keys():
            apps[key][value[0]].append(value[1:])
        else:
            apps[key][value[0]] = [value[1:]]
    for key in apps.keys():
        for path in apps[key]:
            env.add_handlers(key, [(path, handler(dict(apps[key][path])))])
    env.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    start()
