from tornado.testing import *
import unittest
import json
import thunder
import tornado

@thunder.get()
def hello():
    return "hello"

@thunder.get('/headers')
def headers(response):
    response.headers["hello"] = "world"
    return "hello"

@thunder.get('/cookies')
def cookies(response):
    response.cookies["hello"] = "world"
    return "hello"

@thunder.post()
def echo(request):
    return request.body

@thunder.patch()
def echo(request):
    return request.body

@thunder.put()
def echo(request):
    return request.body

@thunder.get('/test/{0}/')
def named(request, param):
    return param

@thunder.get('/other/test/{name}/')
def named(request, name):
    return name

@thunder.get('/other/test/{name}/{age}/')
def mulitple_names(request, age, name):
    return "You are {age} and your name is {name}".format(age=age, name=name)

class ThunderTests(AsyncHTTPTestCase):
    # required setup
    def get_app(self):
        return thunder.make_app()

    def test_http_get(self):
        response = self.fetch('/', method="GET")
        self.assertEqual(b"hello", response.body)

    def test_http_headers_get(self):
        response = self.fetch('/headers', method="GET")
        self.assertEqual("world", response.headers["hello"])

    def test_http_cookies_get(self):
        response = self.fetch('/cookies', method="GET")
        self.assertEqual("hello=world", response.headers["Set-Cookie"].split(';')[0])

    def test_http_post(self):
        response = self.fetch('/', body=json.dumps({"testing":"12"}), method="POST")
        self.assertEqual({"testing":"12"}, json.loads(response.body.decode('utf8')))

    def test_http_put(self):
        response = self.fetch('/', body=json.dumps({"testing":"12"}), method="PUT")
        self.assertEqual({"testing":"12"}, json.loads(response.body.decode('utf8')))

    def test_http_patch(self):
        response = self.fetch('/', body=json.dumps({"testing":"12"}), method="PATCH")
        self.assertEqual({"testing":"12"}, json.loads(response.body.decode('utf8')))

    def test_http_numbered_params(self):
        response = self.fetch('/test/something/', method="GET")
        self.assertEqual(b"something", response.body)

    def test_http_named_params(self):
        response = self.fetch('/other/test/something/', method="GET")
        self.assertEqual(b"something", response.body)

    def test_http_named_params_no_slash(self):
        response = self.fetch('/other/test/something', method="GET")
        self.assertEqual(b"something", response.body)

    def test_http_many_named_params(self):
        response = self.fetch('/other/test/raphael/30/', method="GET")
        self.assertEqual(b"You are 30 and your name is raphael", response.body)

if __name__=="__main__":
    unittest.main()
