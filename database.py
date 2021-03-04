import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS register (firstname TEXT, lastname TEXT, '
                 'email TEXT, mobile_number TEXT, password TEXT)')
    print("Table created successfully")
    conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/enter-new/')
def enter_new_student():
    return render_template('register.html')


@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    msg = None
    try:
        post_data = request.get_json()
        firstname = post_data['firstname']
        lastname = post_data['lastname']
        email = post_data['email']
        mobile_number = post_data['mobile_number']
        password = post_data['password']

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (firstname, lastname, email, mobile_number, password) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (firstname, lastname, email, mobile_number, password))
            con.commit()
            msg = "Record successfully added."

    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + e

    finally:
        return jsonify(msg)
        con.close()


@app.route('/show-records/', methods=['GET'])
def show_records():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM students")
            records = cur.fetchall()

    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database."+ e)
    finally:
        con.close()
        return jsonify(records)


if __name__ == "__main__":
    app.run(debug=True)
