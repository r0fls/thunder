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
    #class Handler(tornado.web.RequestHandler):
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
    return Handler


# Decorators
def get(path='/'):
    '''
    Adds a function and optional path to global env instance
    '''
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
    def _put(func_to_decorate):
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        #env.add_handlers(r".*", [(path, get_handler(func_to_decorate))])
        app.append([r".*", [path, 'put', func_to_decorate]])
    return _put

# move to test
@post('/test')
def echo(request):
    '''echo back the headers'''
    return str(request.body)

# should work with named parameters
#?P<param1>
# move to test
@get('/test/([^\/]+)/')
def headers(request, param1):
    '''echo back the headers'''
    print("Got param: {}".format(param1))
    return str(request.headers)

# this should turn into a capture group
# and pass to the function
#@get('/hello/{str:name}/{int:age}')
#def headers(name, age):
#    '''echo back the headers'''
#    return str("hello, {0}. Are you {1}?".format(name, age))

# move to test
@put('/test')
def put_echo(request):
    '''echo back the headers'''
    return str(request.body)

def prepare():
    apps = defaultdict(dict)
    for key, value in app:
        if value[0] in apps[key].keys():
            apps[key][value[0]].append(value[1:])
        else:
            apps[key][value[0]] = [value[1:]]
    for key in apps.keys():
        for path in apps[key]:
            env.add_handlers(key, [(path, handler(dict(apps[key][path])))])

def start(port=8888):
    prepare()
    env.listen(port)
    return tornado.ioloop.IOLoop.current().start()

def stop():
        env.tornado.ioloop.IOLoop.instance().stop()
if __name__ == "__main__":
    start()
