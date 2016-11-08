#!flask/bin/python
from flask import Flask, jsonify
import psycopg2
import config

try:
    conn = psycopg2.connect("dbname='"+config.database['dbname']+"' user='"+config.database['user']+"' host='"+config.database['host']+"' password='"+config.database['password']+"'")
except:
    print("I am unable to connect to the database")
    
try:
    cur = conn.cursor()
    cur.execute("""SELECT s.id,name,body_diameter,head_diameter,head_height,hexagon_diameter,hexagon_height,thread_length,body_length FROM iso_4762 as s LEFT OUTER JOIN iso_4762_length as l ON s.id = l.sid ORDER BY s.body_diameter ASC, l.body_length ASC""")
    rows = cur.fetchall()
except:
    print("I can't drop our database!")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_tasks():
    return jsonify({'iso_4762': rows})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
