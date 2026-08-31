# rules of a ReST API
# 1. Data is transferred as key value-pairs called JSON.Sending from JS as JSON Object and from python as dictionary
# 2. You must define routes/URL 
# 3. You must define a HTTP method(GET,POST,PUT,DELETE,PATCH)
# 4. You must define a status code(200,201,404,401,500)
# 200 → success,201 → created,400 → bad request,401 → unauthorized, 403-forbidden, 404 — Not Found,409 → conflict (email exists),500 → server error

from flask import Flask,request,jsonify
from sqlalchemy import select
from sqlalchemy.orm import Session

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

app.run(debug=True)