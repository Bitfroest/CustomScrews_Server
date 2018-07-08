#!flask/bin/python
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import config
from flask import g

app = Flask(__name__)
def connect_db():
    try:
        conn = psycopg2.connect("dbname='"+config.database['dbname']+"' user='"+config.database['user']+"' host='"+config.database['host']+"' port='"+config.database['port']+"' password='"+config.database['password']+"'")
        return conn
    except:
        print("I am unable to connect to the database")

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'postgresql'):
        g.postgresql = connect_db()
    return g.postgresql

@app.route('/', methods=['GET'])
def get_tasks():
    try:
        cur = get_db().cursor()
        cur.execute("""SELECT s.id,name,body_diameter,head_diameter,head_height,hexagon_diameter,hexagon_height,thread_length,body_length FROM iso_4762 as s LEFT OUTER JOIN iso_4762_length as l ON s.id = l.sid ORDER BY s.body_diameter ASC, l.body_length ASC""")
        rows = cur.fetchall()
    except:
        print("I can't drop our database!")
    return jsonify({'iso_4762': rows})

@app.route('/users/', methods = ['GET', 'POST'])
def user():
    if request.method == 'GET':
        """return the information for users"""


    if request.method == 'POST':
        data = request.get_json()
        if 'userId' in data:
            sql = """INSERT INTO users(id, email, display_name, name) VALUES (%s,%s,%s,%s) ON CONFLICT("id") DO UPDATE SET email=%s ,display_name=%s,name=%s RETURNING id, email, display_name, name;"""
            id = data.get("userId")
            email = data.get("email", "")
            display_name = data.get("display_name", "")
            name = data.get("name", "")
            cur = get_db().cursor(cursor_factory=RealDictCursor)
            cur.execute(sql, (id,email,display_name,name,email,display_name,name,))
            row = cur.fetchone()
            get_db().commit()
            cur.close()
            return jsonify({'user': row})
    else:
        # POST Error 405 Method Not Allowed
        return

@app.route('/user/<id>/screw/<screw_id>', methods = ['GET', 'PUT'])
def screw(id, screw_id):
    if request.method == 'GET':
        """return the information for users"""
        cur = get_db().cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT s.id,name,body_diameter,head_diameter,head_height,hexagon_diameter,hexagon_height,thread_length,body_length FROM iso_4762 as s LEFT OUTER JOIN iso_4762_length as l ON s.id = l.sid WHERE s.id= %s AND (s.id_users=%s OR s.id_users IS NULL) ORDER BY s.body_diameter ASC, l.body_length ASC""", (screw_id,id,))
        rows = cur.fetchall()
        return jsonify({'iso_4762': rows})

    if request.method == 'PUT':
        data = request.get_json()
        if 'name' in data and 'body_diameter' in data and 'head_diameter' in data and 'head_height' in data and 'hexagon_diameter' in data and 'hexagon_height' in data:
            sql = """UPDATE iso_4762 SET (name, body_diameter, head_diameter, head_height, hexagon_diameter, hexagon_height) = (%s,%s,%s,%s,%s,%s) WHERE id=%s AND id_users=%s RETURNING *;"""
            insert = """INSERT INTO iso_4762 (name, body_diameter, head_diameter, head_height, hexagon_diameter, hexagon_height, id_users) SELECT %s,%s,%s,%s,%s,%s,%s WHERE NOT EXISTS (SELECT 1 FROM iso_4762 WHERE id=%s AND id_users=%s) RETURNING *;"""
            name = data.get("name")
            body_diameter = data.get("body_diameter")
            head_diameter = data.get("head_diameter")
            head_height = data.get("head_height")
            hexagon_diameter = data.get("hexagon_diameter")
            hexagon_height = data.get("hexagon_height")
            thread_length = data.get("thread_length")
            body_length = data.get("body_length")
            cur = get_db().cursor(cursor_factory=RealDictCursor)
            cur.execute(sql, (name, body_diameter, head_diameter, head_height, hexagon_diameter, hexagon_height, screw_id, id,))
            row = cur.fetchone()
            if not row:
                cur.execute(insert, (name, body_diameter, head_diameter, head_height, hexagon_diameter, hexagon_height, id, screw_id, id,))
                row = cur.fetchone()
            get_db().commit()
            cur.close()
            return jsonify({'iso_4762': row})
    else:
        # POST Error 405 Method Not Allowed
        return

@app.route('/user/<id>/screws/', methods = ['GET', 'POST'])
def screws(id):
    if request.method == 'GET':
        """return the information for users"""
        cur = get_db().cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT s.id,name,body_diameter,head_diameter,head_height,hexagon_diameter,hexagon_height,thread_length,body_length FROM iso_4762 as s LEFT OUTER JOIN iso_4762_length as l ON s.id = l.sid WHERE s.id_users=%s OR s.id_users IS NULL ORDER BY s.body_diameter ASC, l.body_length ASC""", (id,))
        rows = cur.fetchall()
        return jsonify({'iso_4762': rows})

    if request.method == 'POST':
        data = request.get_json()
        if 'name' in data and 'body_diameter' in data and 'head_diameter' in data and 'head_height' in data and 'hexagon_diameter' in data and 'hexagon_height' in data:
            sql = """INSERT INTO iso_4762(name, body_diameter, head_diameter, head_height, hexagon_diameter, hexagon_height, id_users) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *;"""
            name = data.get("name")
            body_diameter = data.get("body_diameter")
            head_diameter = data.get("head_diameter")
            head_height = data.get("head_height")
            hexagon_diameter = data.get("hexagon_diameter")
            hexagon_height = data.get("hexagon_height")
            thread_length = data.get("thread_length")
            body_length = data.get("body_length")
            cur = get_db().cursor(cursor_factory=RealDictCursor)
            cur.execute(sql, (name, body_diameter, head_diameter, head_height, hexagon_diameter, hexagon_height, id,))
            row = cur.fetchone()
            get_db().commit()
            cur.close()
            return jsonify({'iso_4762': row})
    else:
        # POST Error 405 Method Not Allowed
        return

@app.route('/screw/<screw_id>/length/', methods = ['GET', 'POST'])
def length(screw_id):
    if request.method == 'POST':
        data = request.get_json()
        if 'thread_length' in data and 'body_length' in data:
            sql = """INSERT INTO iso_4762_length(thread_length, body_length, sid) SELECT %s, %s, %s WHERE EXISTS (SELECT 1 FROM iso_4762 WHERE id=%s) RETURNING *;"""
            thread_length = data.get("thread_length")
            body_length = data.get("body_length")
            cur = get_db().cursor(cursor_factory=RealDictCursor)
            cur.execute(sql, (thread_length,body_length,screw_id,screw_id,))
            row = cur.fetchone()
            get_db().commit()
            cur.close()
            return jsonify({'iso_4762_length': row})
    else:
        # POST Error 405 Method Not Allowed
        return


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
