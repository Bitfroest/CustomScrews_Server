#!flask/bin/python
from flask import Flask, jsonify
import psycopg2
import config

try:
    conn = psycopg2.connect("dbname='"+config.database['dbname']+"' user='"+config.database['user']+"' host='"+config.database['host']+"' password='"+config.database['password']+"'")
except:
    print("I am unable to connect to the database")
    
cur = conn.cursor()
try:
    cur.execute("""SELECT * from iso_4762 as i ORDER BY i.body_diameter ASC, i.body_length ASC""")
    rows = cur.fetchall()
except:
    print("I can't drop our database!")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_tasks():
    return jsonify({'iso_4762': rows})

if __name__ == '__main__':
    app.run(debug=True)
