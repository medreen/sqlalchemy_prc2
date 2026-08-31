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
from datetime import datetime

from models import User,Product,Sale,Sales_detail,Purchase,Payment, engine, Base
import json

app = Flask(__name__)
session = Session(engine)

user = {"id": '1',
        "full_name":"Binti",
        "email":"binti@gmail.com",
        "password":"binti5",
        "phone_number":"0717238745"}

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

        if not data.get('full_name') or not data.get('email') or not data.get('password') or not data.get('phone_number'):
            return jsonify({'err': 'Ensure all fields are set'}), 400

        # check if email already exists
        stmt = select(User).where(User.email == data['email'])
        existing_user = session.scalars(stmt).first()
        if existing_user:
            return jsonify({'err': 'Email already registered'}), 409

        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            full_name=data['full_name'],
            email=data['email'],
            password=hashed_password,
            phone_number=data['phone_number']
        )
        session.add(new_user)
        session.commit()  

        return jsonify({'message': 'User added successfully'}), 201
    else:
        return jsonify({'err': 'Method not allowed'}), 405


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return jsonify({'err': 'Ensure all fields are set'}), 400

        user_email = data['email']
        stmt = select(User).where(User.email == user_email)
        user = session.scalars(stmt).first()

        if user and check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'err': 'Invalid email or password'}), 401
    else:
        return jsonify({'err': 'Method not allowed'}), 405


@app.route("/products", methods = ['GET', 'POST'])
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
            error = {"error":"Ensure all fields are set"}
            return jsonify(error), 403
        else:
            new_product = Product(user_id = user['id'], product_name=data['product_name'], buying_price=data['buying_price'], selling_price=data['selling_price'])
            session.add(new_product)
            session.commit()
            return jsonify({"message":"Product created successfully"}), 201
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == 'GET':
        query = select(Sale)
        sales = session.scalars(query)

        results = []
        for sale in sales:
            s = {"id" : sale.id, "user_id" : user['id'], "created_at" : sale.created_at}
            results.append(s)
        return jsonify(results), 200

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            error = {'err' : 'Ensure all fields are set'}
        else:
            new_sale = Sale(user_id=user['id'], created_at=datetime.now())
            session.add(new_sale)
            session.commit()
            return jsonify({'message' : 'Sale created successfully'})
    else:
        error = {'error': 'Method not allowed'}
        return jsonify(error), 405

@app.route('/sales-details', methods=['GET', 'POST'])
def sales_details():
    if request.method == 'GET':
        query = select(Sales_detail)
        sales_details = session.scalars(query)

        results = []
        for detail in sales_details:
            d = {"id" : detail.id, "product_id" : detail.product_id, "sale_id" : detail.sale_id, "quantity" : detail.quantity, "created_at" : detail.created_at}
            results.append(d)
        return jsonify(results), 200

    elif request.method == 'POST':
        data = request.get_json()
        if data['product_id'] == '' or data['sale_id'] == '' or data['quantity'] == '':
            error = {'err' : 'Ensure all fields are set'}
            return jsonify(error), 403
        else:
            new_detail = Sales_detail(product_id=data['product_id'], sale_id=data['sale_id'], quantity=data['quantity'], created_at=datetime.now())
            session.add(new_detail)
            session.commit()
            return jsonify({'message' : 'Sales detail created successfully'}), 201
    else:
        error = {'error': 'Method not allowed'}
        return jsonify(error), 405

@app.route('/purchases', methods=['GET', 'POST'])
def purchases():
    if request.method == 'GET':
        query = select(Purchase)
        purchases = session.scalars(query)

        results = []
        for purchase in purchases:
            p = {"id" : purchase.id, "product_id" : purchase.product_id, "quantity" : purchase.quantity, "buying_price" : purchase.buying_price, "created_at" : purchase.created_at}
            results.append(p)
        return jsonify(results), 200

    elif request.method == 'POST':
        data = request.get_json()
        if data['product_id'] == '' or data['quantity'] == '' or data['buying_price'] == '':
            error = {'err' : 'Ensure all fields are set'}
            return jsonify(error), 403
        else:
            new_purchase = Purchase(product_id=data['product_id'], quantity=data['quantity'], buying_price=data['buying_price'], created_at=datetime.now())
            session.add(new_purchase)
            session.commit()
            return jsonify({'message' : 'Purchase created successfully'}), 201
    else:
        error = {'error': 'Method not allowed'}
        return jsonify(error), 405

@app.route('/payments', methods=['GET', 'POST'])
def payments(): 
    if request.method == 'GET':
        query = select(Payment)
        payments = session.scalars(query)

        results = []
        for payment in payments:
            p = {"id" : payment.id, "sale_id" : payment.sale_id, "amount" : payment.amount, "payment_method" : payment.payment_method, "payment_status" : payment.payment_status, "created_at" : payment.created_at}
            results.append(p)
        return jsonify(results), 200

    elif request.method == 'POST':
        data = request.get_json()
        if data['sale_id'] == '' or data['amount'] == '' or data['payment_method'] == '' or data['payment_status'] == '':
            error = {'err' : 'Ensure all fields are set'}
            return jsonify(error), 403
        else:
            new_payment = Payment(sale_id=data['sale_id'], amount=data['amount'], payment_method=data['payment_method'], payment_status=data['payment_status'], created_at=datetime.now())
            session.add(new_payment)
            session.commit()
            return jsonify({'message' : 'Payment created successfully'}), 201
    else:
        error = {'error': 'Method not allowed'}
        return jsonify(error), 405


app.run(debug=True)