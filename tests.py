from tornado.testing import *
import unittest
import json
import thunder
import tornado

@thunder.get()
def hello():
    return "hello"

@thunder.post()
def echo(request):
    return request.body

@thunder.put()
def echo(request):
    return request.body


class ThunderTests(AsyncHTTPTestCase):
    # required setup
    def get_app(self):
        thunder.prepare()
        return thunder.env

    # test get
    def test_http_get(self):
        response = self.fetch('/', method="GET")
        self.assertEqual("hello", response.body)

    def test_http_post(self):
        response = self.fetch('/', body=json.dumps({"testing":"12"}), method="POST")
        self.assertEqual({"testing":"12"}, json.loads(response.body))

    def test_http_put(self):
        response = self.fetch('/', body=json.dumps({"testing":"12"}), method="PUT")
        self.assertEqual({"testing":"12"}, json.loads(response.body))

if __name__=="__main__":
    unittest.main()
