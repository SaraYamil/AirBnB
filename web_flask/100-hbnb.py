#!/usr/bin/python3

'''
A simple Flask web application.
'''

from flask import Flask
from flask import render_template, Markup
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb')
def hbnb():
    '''
    Displays an HTML page with a list of all State objects in DBStorage.
    '''
    every_state = list(storage.all(State).values())
    all_amenities = list(storage.all(Amenity).values())
    all_places = list(storage.all(Place).values())
    every_state.sort(key=lambda x: x.name)
    all_amenities.sort(key=lambda x: x.name)
    all_places.sort(key=lambda x: x.name)

    for state in every_state:
        state.cities.sort(key=lambda x: x.name)

    for place in all_places:
        place.description = Markup(place.description)

    txt = {
        'states': every_state,
        'amenities': all_amenities,
        'places': all_places
    }

    return render_template('100-hbnb.html', **txt)


@app.teardown_appcontext
def flask_teardown(exc):
    '''
    Closes the current SQLAlchemy session.
    '''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
