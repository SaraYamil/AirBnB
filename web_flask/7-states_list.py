#!/usr/bin/python3

'''
A script that starts a Flask web application
'''
from flask import Flask, render_template

from models.state import State
from models import storage


app = Flask(__name__)
'''The Flask application instance.'''
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    '''Displays an HTML page with a list of all State objects in DBStorage.'''
    states = list(storage.all(State).values())
    states.sort(key=lambda x: x.name)
    txt = {
        'states': states
    }

    return render_template('7-states_list.html', **txt)


@app.teardown_appcontext
def flask_teardown(exc):
    '''Closes the current SQLAlchemy session.'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
