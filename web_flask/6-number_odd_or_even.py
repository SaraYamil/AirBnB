#!/usr/bin/python3

'''A script that starts a Flask web application'''

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    return "C " + text.replace("_", " ")


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text):
    return "Python " + text.replace("_", " ")


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    if isinstance(n, int):
        if n % 2 == 0:
            parity = "even"
        else:
            parity = "odd"
        return render_template('6-number_odd_or_even.html', n=n, parity=parity)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
