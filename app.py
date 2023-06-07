from flask import Flask, request, jsonify, abort, json, g, Response
import sqlite3


app = Flask(__name__)


@app.route('/')
def welcome():
   return 'Welcome to the movie database.'


@app.route('/movies', methods=["GET", "POST"])
def get_or_add_movies():
    if request.method == 'GET':

        cur = g.db.cursor()
        cur.execute("SELECT * FROM MOVIES")
        movies = cur.fetchall()
        return jsonify(movies)

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
            g.db.execute('INSERT INTO MOVIES (TITLE,DESCRIPTION,RELEASE_YEAR) VALUES (?, ?, ?)',
                        (title, description, release_year))
            g.db.commit()

            return Response('', 200)


@app.route('/movies/<int:id>', methods=["GET", "PUT"])
def get_or_put_movie(id):

    if request.method == 'GET':
        cur = g.db.cursor()
        cur.execute("SELECT * FROM MOVIES WHERE id = ?", (id,))
        movie = cur.fetchone()

        """ Wrong index """
        if movie is None:
            abort(404)
        else:
            return jsonify(movie)

    elif request.method == 'PUT':

        """ Data extraction """
        data = get_json_data_safely(request)
        title = data['title']
        description = data['description']
        release_year = data['release_year']

        cur = g.db.cursor()
        cur.execute("SELECT * FROM MOVIES WHERE id = ?", (id,))
        movie = cur.fetchone()

        """ Wrong index """
        if movie is None:
            abort(404)
        else:

            """ Update query """
            g.db.execute('UPDATE MOVIES SET TITLE = ?, DESCRIPTION = ?, RELEASE_YEAR = ? WHERE id = ?',
                             (title, description, release_year, id))
            g.db.commit()
            return Response('', 200)

@app.before_request
def before_request():
    g.db = sqlite3.connect('test.db')

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def get_json_data_safely(request):
    """ Accepting json or text-plain"""
    if request.is_json:
        data = request.json
    else:
        data = json.loads(request.data)
    return data


if __name__ == '__main__':
    app.run()
