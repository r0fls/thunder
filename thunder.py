import tornado.ioloop
import tornado.web
import inspect

env = tornado.web.Application()

def get_handler(function):
    '''
    Returns a tornado handler with get method defined by the function passed
    via the get decorator
    '''
    class Handler(tornado.web.RequestHandler):
        def get(self):
            if len(inspect.getargspec(function).args) == 0:
                self.write(function())
            elif len(inspect.getargspec(function).args) == 1:
                self.write(function(self.request))
    return Handler


# should take optional arguments for path
def get(path='/'):
    '''
    Adds a function and optional path to global env instance
    '''
    # this should match against existing env and append to existing ones
    def _get(func_to_decorate):
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        #if env.
        env.add_handlers(r".*", [(path, get_handler(func_to_decorate))])
    return _get

def put_handler(function):
    class Handler(tornado.web.RequestHandler):
        def put(self):
            if len(inspect.putargspec(function).args) == 0:
                self.write(function())
            elif len(inspect.putargspec(function).args) == 1:
                self.write(function(self.request))
    return Handler


# should take optional arguments for path
def put(path='/'):
    def _put(func_to_decorate):
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        env.add_handlers(r".*", [(path, put_handler(func_to_decorate))])
    return _put



def post_handler(function):
    class Handler(tornado.web.RequestHandler):
        def post(self):
            if len(inspect.postargspec(function).args) == 0:
                self.write(function())
            elif len(inspect.postargspec(function).args) == 1:
                self.write(function(self.request))
    return Handler


# should take optional arguments for path
def post(path='/'):
    def _post(func_to_decorate):
        def new_func(*original_args, **original_kwargs):
            return func_to_decorate(*original_args, **original_kwargs)
        env.add_handlers(r".*", [(path, post_handler(func_to_decorate))])
    return _post

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
    import pdb; pdb.set_trace()
    env.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    start()
