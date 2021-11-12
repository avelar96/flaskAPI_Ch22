
from flask import Flask, abort, render_template, request
from moc_data import mock_data
from flask_cors import CORS  # pip install flask-cors
from config import db, json_parse
import json
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # allows anyone to call the server (**DANGER**)


coupon_codes = [
    {
        "code": "qwerty",
        "discount": 10
    }
]

me = {
    "name": "Martin",
    "last": "Avelar",
    "age": 35,
    "hobbies": [],
    "email": "abc@gmail.com",
    "address": {
        "street": "Evergreen",
        "city": "Springfield",
    }
}


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/test")
def test():
    return "Hello there!"

# / about


@app.route("/about")
def about():
    # return full name
    return me["name"] + " " + me["last"]


# / about email
@app.route("/about/email")
def email():
    return me["email"]

# / about address


@app.route("/about/address")
def address():
    return me["address"]


#####API METHODS#####


@app.route("/api/catalog", methods=["get"])
def get_catalog():
    # returns catalog as JSON
    # find with no filter = get all data in the collection
    cursor = db.products.find({})
    catalog = []
    for prod in cursor:
        catalog.append(prod)

    # inv homework:python list comprehension

    print(len(catalog), "Record obtained form db")

    return json_parse(catalog)


@app.route("/api/catalog", methods=["post"])
def save_product():
    # get request payload (body)
    product = request.get_json()

    # validate that title exists in dict,if not abort(404)
    if not 'title' in product or len(product["title"]) < 5:
        # 400 = bad request
        # 404 bad request
        return abort(400, "Title is required, and should contain at least 5 chars")

    # validate that price exist and is greater than 0
    if not 'price' in product:
        return abort(400, "Price is required")

    if not isinstance(product["price"], float) and not isinstance(product["price"], int):
        return abort(400, "Price should a valid float number")

    if product['price'] <= 0:
        return abort(400, "Price should be greater than 0")

    # save the product
    db.products.insert_one(product)

    # return the saved object
    return json_parse(product)


@app.route("/api/categories", methods=["GET"])
def get_categories():
    # return the list (string) of unique categories
    categories = []
    cursor = db.products.find({})
    for prod in cursor:
        if not prod["category"] in categories:
            categories.append(prod["category"])
    # logic
    return json_parse(categories)


@app.route("/api/product/<id>")
def get_product(id):
    product = db.products.find_one({"_id": ObjectId(id)})
    if not product:
        return abort(404)  # 404 = Not Found

    return json_parse(product)


# /api/catalog<category>
# return all the products that belong to that cat
@app.route("/api/catalog/<category>")
def get_by_category(category):
    cursor = db.products.find({"category": category})
    list = []
    for prod in cursor:
        list.append(prod)

    return json_parse(list)


# /api/cheapest
# cheapest product

@app.route("/api/cheapest")
def cheapest_product():
    cursor = db.products.find({})
    pivot = cursor[0]
    for prod in cursor:
        if prod["price"] < pivot["price"]:
            pivot = prod

    return json_parse(pivot)


###Orders###

@app.route("/api/order", methods=["POST"])
def save_order():
    # get the order object from the request
    order = request.get_json()
    if order is None:
        return abort(400, "Nothing to save")

    # validations

    # save the object in the database (orders collection)
    db.orders.insert_one(order)
    # return the stored object
    return json_parse(order)


###coupon codes###

# Post to /api/couponCodes
@app.route("/api/couponCodes", methods=["POST"])
def save_coupon():
    coupon = request.get_json()

    # validation
    if not "code" in coupon or len(coupon["code"]) < 5:
        return abort(400, "Code is required, should contain 5 characters")
    # save
    db.couponCodes.insert_one(coupon)
    return json_parse(coupon)

# GET to /api/couponCodes


@app.route("/api/couponCodes", methods=["GET"])
def get_coupons():
    cursor = db.couponCodes.find({})
    all_coupons = []
    for cp in cursor:
        all_coupons.append(cp)

    return json_parse(all_coupons)

# get coupon by its code or 404


@app.route("/api/couponCodes/<code>")
def get_coupon_by_code(code):
    # get the coupon from db
    coupon = db.couponCodes.find_one({"code": code})
    # if it is none return 404 error
    if coupon is None:
        return abort(404, "Invalid coupon code")

    return json_parse(coupon)


@app.route("/test/onetime/filldb")
def fill_db():
    # iterate the mock_data list
    for prod in mock_data:
        # save every object to db.products
        prod.pop("_id")  # remove the id from dict/product
        db.products.insert_one(prod)  # stores

    return "Done!"


# start the application
# debug true
app.run(debug=True)
