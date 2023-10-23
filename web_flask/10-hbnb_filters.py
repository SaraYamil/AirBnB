#!/usr/bin/python3

'''
A simple Flask web application.
'''

from flask import Flask, render_template
from models.amenity import Amenity
from models.state import State
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb_filters')
def hbnb_filters():
    '''
    Displays an HTML page with a list of all State objects in DBStorage.
    '''
    all_states = list(storage.all(State).values())
    amenities = list(storage.all(Amenity).values())
    all_states.sort(key=lambda x: x.name)
    amenities.sort(key=lambda x: x.name)
    for state in all_states:
        state.cities.sort(key=lambda x: x.name)

    txt = {
        'states': all_states,
        'amenities': amenities
    }

    return render_template('10-hbnb_filters.html', **txt)


@app.teardown_appcontext
def flask_teardown(exc):
    '''
    Closes the current SQLAlchemy session.
    '''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
