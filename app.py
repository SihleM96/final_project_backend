import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText


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
    print("User Table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS products (image TEXT, product_name TEXT, category TEXT, product_price INTEGER, description TEXT)')
    print("Products Table created successfully")
    conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)


# @app.route('/')
# @app.route('/enter-new/')
# def enter_new_student():
#     return render_template('register.html')


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
            cur.execute("INSERT INTO register (firstname, lastname, email, mobile_number, password) "
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
            cur.execute("SELECT * FROM register")
            records = cur.fetchall()

    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database." + e)
    finally:
        con.close()
        return jsonify(records)


# PRODUCTS IMAGE API
#INSERT PRODUCTS INTO DB
@app.route('/products/')
def get_products():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("INSERT INTO products (image, product_name, category, product_price, description) VALUES('https://i.postimg.cc/KcdCgnRw/vase1.jpg','Salty', 'vase', '500', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category, product_price, description) VALUES( 'https://i.postimg.cc/jjsKGkSg/vase2.jpg','Hollow Lily', 'vase', '540', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category,  product_price, description) VALUES('https://i.postimg.cc/YSG1gm4D/vase3.jpg','Dusty', 'vase', '550', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category,product_price, description) VALUES( 'https://i.postimg.cc/VNCC5QT3/vase4.jpg','Omari', 'vase', '500', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category, product_price, description) VALUES('https://i.postimg.cc/GhmCMggT/bowl1.jpg','Night Skies', 'bowl', '430', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category,product_price, description) VALUES('https://i.postimg.cc/05MysdTB/bowl2.jpg','Blue Velvet', 'bowl', '400', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category, product_price, description) VALUES('https://i.postimg.cc/ZqGDymq3/bowl3.jpg','Azizi', 'bowl', '400', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category, product_price, description) VALUES('https://i.postimg.cc/F1X9P8GJ/bowl4.jpg','OLiver', 'bowl', '420', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category, product_price, description) VALUES( 'https://i.postimg.cc/wvtynK5W/cup1.jpg','Malifa', 'cup', '200', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category,product_price, description) VALUES('https://i.postimg.cc/sgwMXfw6/cup2.jpg','Nkungu', 'cup', '250', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category, product_price, description) VALUES('https://i.postimg.cc/ryxz4Nft/cup3.jpg','Misty', 'cup', '230', 'Lorem ipsum dolor sit amet')")
            cur.execute("INSERT INTO products (image, product_name, category, product_price, description) VALUES( 'https://i.postimg.cc/wjfBzfjn/cup4.jpg','Iseult', 'cup', '200', 'Lorem ipsum dolor sit amet')")
            con.commit()
            msg = "added records"
    except Exception as e:
        con.rollback()
        msg = "error occurred insert operation" + str(e)
    finally:
        con.close()
        return jsonify(msg)


# GET ALL PRODUCTS
# SHOW DB IMAGES

@app.route('/show_products/', methods=['GET'])
def show_products():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM products")
            records = cur.fetchall()

    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the product database." + e)
    finally:
        con.close()
        return jsonify(records)


# #     GET SINGLE PRODUCT
# @app.route('/products/<int: product_id>', methods=['GET'])
# def show_product(product_id):
#     record = {}
#     try:
#         with sqlite3.connect('database.db') as con:
#             con.row_factory = dict_factory
#             cur = con.cursor()
#             cur.execute("SELECT * FROM products WHERE product_id=" + str(product_id))
#             record = cur.fetchone()
#
#     except Exception as e:
#         con.rollback()
#         print("There was an error fetching results from the product database." + e)
#     finally:
#         con.close()
#         return jsonify(record)

if __name__ == "__main__":
    app.run(debug=True)
