[![Build Status](https://travis-ci.org/r0fls/thunder.png)](https://travis-ci.org/r0fls/thunder)
# thunder
api decorators for tornado

See branch v0.1.0 for a stable release.

##Examples

**In tradition:**
```
@thunder.get()
def hello():
    return "hello, world"

thunder.run(80)
```

```
$ curl localhost
```

**More interesting:**
```
@thunder.get('/hello/{name}')
def hello(name):
    return "Hello, {}".format(name)
    
thunder.run(80)
```

```
$ curl localhost/hello/luke
```

**Using request object**

```
@thunder.get('/hello/{name}')
def hello(request, name):
    return "Hello, {name}. These are your headers: {headers}".format(name=name,
                                                                     headers=request.headers)

thunder.run(80)
```

```
$ curl localhost/hello/luke
```

**Using response object**

```
@thunder.get('/hello/{name}')
def hello(response, name):
    response.headers["hello"] = "world"
    response.cookies["user"] = name
    response.code = 204
    return

thunder.run(80)
```

```
curl -i localhost/hello/wookie
```

You can also use `post`, `put`, `delete` and `patch`.
