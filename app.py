from flask import Flask, request, jsonify, abort, json, g, Response
import sqlite3


app = Flask(__name__)


@app.route('/')
def welcome():
   return 'Welcome to the movie database.'


@app.route('/movies', methods=["GET", "POST"])
def get_or_add_movies():
    """ First and third task """
    if request.method == 'GET':

        cur = g.db.cursor()
        cur.execute("SELECT * FROM MOVIES ORDER BY id")
        rows = cur.fetchall()

        json_output = json.dumps(serialize_data(rows), sort_keys=False)
        return Response(json_output, mimetype='application/json')

    elif request.method == 'POST':

        """ Data extraction """
        data = get_json_data_safely(request)
        title = data['title']
        description = data['description']
        release_year = data['release_year']

        """ Required data """
        if not title:
            abort(404)
        elif not release_year:
            abort(404)

        else:
            """ Data insertion """
            g.db.execute('INSERT INTO MOVIES (TITLE,DESCRIPTION,RELEASE_YEAR) VALUES (?, ?, ?)',
                         (title, description, release_year))
            g.db.commit()

            return Response('', 200)


@app.route('/movies/<int:id>', methods=["GET", "PUT"])
def get_or_put_movie(id):

    """ Second and fourth task """
    if request.method == 'GET':
        """ Movie selection """
        cur = g.db.cursor()
        cur.execute("SELECT * FROM MOVIES WHERE id = ?", (id,))
        row = cur.fetchall()

        """ Wrong index """
        if len(row) == 0:
            abort(404)
        else:
            json_output = json.dumps(serialize_data(row), sort_keys=False)
            return Response(json_output, mimetype='application/json')

    elif request.method == 'PUT':

        """ Data extraction """
        data = get_json_data_safely(request)
        title = data['title']
        description = data['description']
        release_year = data['release_year']

        """ Movie selection"""
        cur = g.db.cursor()
        cur.execute("SELECT * FROM MOVIES WHERE id = ?", (id,))
        movie = cur.fetchone()

        """ Wrong index """
        if len(movie) == 0:
            abort(404)
        else:

            """ Update query """
            g.db.execute('UPDATE MOVIES SET TITLE = ?, DESCRIPTION = ?, RELEASE_YEAR = ? WHERE id = ?',
                             (title, description, release_year, id))
            g.db.commit()
            return Response('', 200)


@app.before_request
def before_request():
    """ Connect to DB before calling a method"""
    g.db = sqlite3.connect('test.db')


@app.teardown_request
def teardown_request(exception):
    """ Close DB connection after teardown"""
    if hasattr(g, 'db'):
        g.db.close()


def get_json_data_safely(req):
    """ Accepting json or text-plain"""
    if req.is_json:
        data = req.json
    else:
        data = json.loads(req.data)
    return data


def serialize_data(data):
    """ For prettier visualisation"""
    serialized_movies = []
    for row in data:
        movie = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'release_year': row[3]
        }
        serialized_movies.extend([movie])
    return serialized_movies


if __name__ == '__main__':
    app.run()
