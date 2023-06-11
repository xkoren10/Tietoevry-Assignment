# Python-based micorservice - Assignment 1
## Matej Koreň, 7.6.2023

<h1> Task </h1>
Create a simple REST API using the Flask framework in Python with following endpoints:

1. GET /movies - returns a list of all the movies in the database,
2. GET /movies/\<int:id\> return the details of a movie with the given id,
3. POST /movies - creating a new movie in the database,
4. PUT /movies/\<int:id\> - updates a movie with the given id.


<h2> Solution </h2>
<h3> Data storage </h3>

To store data permanently, sqlite3 database (which is included with Python) was used. It's initialization
script can be seen in the included file *db_init.py*, containing table creation and value constraints for 
each column. In the *app.py* script this database is accessed via sqlite3 library and it's functions.
To read or write into it is possible to use standard SQL queries. 

<h3> Application </h3>

In the solution, two app routes are used - **/movies** for 1. and 3. endpoint and **/movies/\<int:id>** 
for 2. and 4. endpoint. Depending on the HTTP request type, different actions are executed above the database
and proper data are stored or returned. Each method is also documented and described within the code.
To achieve desired output, data serialization with *json.dump* library was necessary.

<h2> Testing </h2>

To use the application, only Flask is needed. To install it, simply use:
>pip install flask

command or download it to your favourite IDE. After this, use:

>python app.py

(or run it in the editor) which should build the app and run it on the loopback adress
(http://127.0.0.1:5000 or http://localhost:5000)

One of the possibilities to test the endpoints is to use **curl** utility. 

For each endpoints the command would look like this:
1. > curl "localhost:5000/movies"
2. > curl "localhost:5000/movies/1"
3. > curl -X POST -H "Content-type: application/json" -d "{\"title\":\"Shrek\",\"description\":\"Shrek, an ogre, embarks on a journey with a donkey to rescue Princess Fiona...\",\"release_year\":\"2001\"}" "localhost:5000/movies"
4. > curl -X PUT -H "Content-type: application/json" -d "{\"title\":\"Shrek\",\"description\":\"Shrek, an ogre, embarks on a
 journey with a donkey to rescue Princess Fiona...\",\"release_year\":\"2023\"}" "localhost:5000/movies/10"

**NOTES**   
Simple **GET** requests can be generated in the browser. **curl** also supports pipelining,
therefore it accepts a JSON file in the *-d* argument, such as
> curl ... -d @new_movie.json ...

