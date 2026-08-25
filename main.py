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
        stmt = select(Product)
        products = session.scalars(stmt)
    elif request.method == 'POST':
        # store the data in a variable
        data = request.get_json()
        if data['product_name'] == '' or data['buying_price'] == '' or data['selling_price'] == '':
            error = {"Error":"Ensure all fields are set"}
            return jsonify(error), 403
        else:
            pass
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

app.run(debug=True)