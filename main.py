# rules of a ReST API
# 1. Data is transferred as key value-pairs called JSON.Sending from JS as JSON Object and from python as dictionary
# 2. You must define routes/URL 
# 3. You must define a HTTP method(GET,POST,PUT,DELETE,PATCH)
# 4. You must define a status code(200,201,404,401,500)
# 200 → success,201 → created,400 → bad request,401 → unauthorized, 403-forbidden, 404 — Not Found,409 → conflict (email exists),500 → server error

from flask import Flask,request,jsonify
from sqlalchemy import select
from sqlalchemy.orm import Session
from flask_bcrypt import generate_password_hash, check_password_hash

from models import User,Product,Sale,Sales_detail,Purchase,Payment, engine, Base
import json

app = Flask(__name__)
session = Session(engine)

@app.route("/")
def home():
    if request.method == "GET":
        data = {"Flask API":"Version 1"}
        return jsonify(data), 200
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        data = request.get_json()
        if data['full_name'] == '' or data['email'] == '' or data['password'] == '' or data['phone_number'] == '':
            err = {'err' : 'Ensure all fields are set'}
            return jsonify(err), 405
        else:
            user_pass = data['password']
            hashed_password = generate_password_hash(user_pass)
            new_user = User(full_name=data['full_name'], email=data['email'], password=hashed_password, phone_number=data['phone_number'])
            session.add(new_user)
            return jsonify({'message' : 'User added successfully'}), 201
    else:
        error = {"err":"Method not allowed"}
        return jsonify(error), 405


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        if data['email'] == '' or data['password'] == '':
            err = {'err' : 'Ensure all fields are set'}
            return jsonify(err), 405
        else:
            user_email = data['email']
            stmt = select(User).where(User.email == user_email)
            user = session.scalars(stmt)

            if user:
                user_pass = data['password']
                if check_password_hash(user.password,user_pass):
                    return jsonify({'message' : 'Login successful'}), 200
    else:
        error = {"err":"Method not allowed"}
        return jsonify(error), 405


@app.route("/products")
def products():
    if request.method == 'GET':
        # fetch the list of all products from the database
        stmt = select(Product)
        products = session.scalars(stmt)

        results = []
        for prod in products:
            p = {"id" : prod.id, "product name" : prod.product_name, "buying price" : prod.buying_price, "selling price" : prod.selling_price}
            results.append(p)
        return jsonify(results), 200

    elif request.method == 'POST':
        # store the data in a variable
        data = request.get_json()
        if data['product_name'] == '' or data['buying_price'] == '' or data['selling_price'] == '':
            error = {"Error":"Ensure all fields are set"}
            return jsonify(error), 403
        else:
            new_product = Product(product_name=data['product_name'], buying_price=data['buying_price'], selling_price=data['selling_price'])
            session.add(new_product)
            session.commit()
            return jsonify({"message":"Product created successfully"}), 201
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == 'GET':
        stmt = select(Sale)
        sales = session.scalars(stmt)

        sales_list = []
        for sale in sales:
            s = {
                "id": sale.id,
                "user_id": sale.user_id,
                "sale_date": sale.sale_date
            }
            sales_list.append(s)
            return jsonify(sales_list), 200


    elif request.method == 'POST':
        data = request.get_json()
        if data['sale_date'] == '':
            error = {'err' : 'Ensure all fields are set'}
        else:
            new_sale = Sale(sale_date=data['sale_date'])
            session.add(new_sale)
            session.commit()
            return jsonify({'message' : 'Sale created successfully'})
    else:
        error = {'error': 'method not allowed'}
        return jsonify(error), 405




app.run(debug=True)