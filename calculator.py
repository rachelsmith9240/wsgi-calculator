"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def homepage():
    """ Tells the user how to use this web app """
    body = '''
<h1>Welcome to the Calculator</h1>
    <p>This calculator allows you to add, subtract, divide, and multiply.</p>
    <p>To use it, enter a URL like this: http://localhost:8080/multiply/3/5</p>
    <p>This URL will calculate 3 x 5 for you.</p>
    <ul>Your options include:
        <li>add</li>
        <li>subtract</li>
        <li>multiply</li>
        <li>divide</li>
    </ul>
'''
    return body


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    result = 0
    try:
        result = sum(map(int, args))
        body = str(result)
    except ValueError:
        body = f"Value Error. Please enter integers as arguments. You entered: {args}." 
    return body

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    result = 0
    try:
        result = list(map(int, args))
        result = result[0] - result[1]
        body = str(result)
    except ValueError:
        body = f"Value Error. Please enter integers as arguments. You entered: {args}." 
    return body

def multiply(*args):
    """ Returns a STRING with the multiplication of the arguments """
    result = 0
    try:
        result = list(map(int, args))
        result = result[0] * result[1]
        body = str(result)
    except ValueError:
        body = f"Value Error. Please enter integers as arguments. You entered: {args}." 
    return body


def divide(*args):
    """ Returns a STRING with the sum of the arguments """
    result = 0
    try:
        result = list(map(int, args))
        result = result[0]*1.0 / result[1]
        body = str(result)
    except ValueError:
        body = f"Value Error. Please enter integers as arguments. You entered: {args}." 
    except ZeroDivisionError:
        body = f"Zero Division Error. Please enter a nonzero denominator. You entered: {args}."
    return body

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    funcs = {
        '': homepage,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "500 Internal Server Errord"
        body = "<h1>Zero Division Error</h1>"
        print(traceback.format_exc())
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
