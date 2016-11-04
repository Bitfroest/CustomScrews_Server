#!flask/bin/python
from flask import Flask, jsonify
import psycopg2

try:
    conn = psycopg2.connect("dbname='screws' user='postgres' host='localhost' password='fakemail'")
except:
    print("I am unable to connect to the database")
    
cur = conn.cursor()
try:
    cur.execute("""SELECT * from iso_4762 as i ORDER BY i.body_diameter ASC, i.body_length ASC""")
    rows = cur.fetchall()
except:
    print("I can't drop our database!")

app = Flask(__name__)

@app.route('/screws', methods=['GET'])
def get_tasks():
    return jsonify({'iso_4762': rows})

if __name__ == '__main__':
    app.run(debug=True)