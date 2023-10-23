#!/usr/bin/python3

'''
A script that starts a Flask web application
'''

from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)
'''The Flask application instance.'''
app.url_map.strict_slashes = False


@app.route('/states')
@app.route('/states/<id>')
def states(id=None):
    '''
    Displays an HTML page with a list of all State objects in DBStorage.
    If id is not None, displays an HTML page with a list of all City objects
    linked to the State with the given id.
    '''
    states = None
    state = None
    every_state = list(storage.all(State).values())
    case = 404
    if id is not None:
        result = list(filter(lambda x: x.id == id, every_state))
        if len(result) > 0:
            state = result[0]
            state.cities.sort(key=lambda x: x.name)
            case = 2
    else:
        states = every_state
        for state in states:
            state.cities.sort(key=lambda x: x.name)
        states.sort(key=lambda x: x.name)
        case = 1
    txt = {
        'states': states,
        'state': state,
        'case': case
    }

    return render_template('9-states.html', **txt)


@app.teardown_appcontext
def flask_teardown(exc):
    '''Closes the current SQLAlchemy session.'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
