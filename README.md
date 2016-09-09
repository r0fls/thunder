# thunder
api decorators for tornado

##Examples

**In tradition:**
```
@thunder.get()
def hello():
    return "hello, world"

thunder.run()
```

```
$ curl localhost
```

**More interesting:**
```
@thunder.get('/hello/{name}')
def hello(name):
    return "Hello, {}".format(name)
    
thunder.run()
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

thunder.run()
```

```
$ curl localhost/hello/luke
```

You can also use `post`, `put`, `delete` and `patch`.
