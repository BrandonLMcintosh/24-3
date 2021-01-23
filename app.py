from flask import Flask, request, jsonify, render_template
from models import connect_db, db, Cupcake
from secret_key import secret_key
from seed import seed_db

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

seed_db(app)

@app.route('/')
def get():
    
    return render_template('index.html')

@app.route('/api/cupcakes', methods=["GET", "POST"])
def cupcakes():
    if request.method == "GET":

        cupcakes = Cupcake.get(all=True)

        return jsonify(cupcakes)
    
    elif request.method == "POST":

        flavor = request.json['flavor']
        size = request.json['size']
        rating = request.json['rating']
        image = request.json['image']

        response = Cupcake.post(flavor=flavor, size=size, rating=rating, image=image)

        return jsonify(response)

        

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["GET", "PATCH", "DELETE"])
def cupcakes_get(cupcake_id):
    

    if request.method == "GET":

        response = Cupcake.get(id=cupcake_id)

        return jsonify(response)

    elif request.method == "PATCH":

        flavor = request.json['flavor']
        size = request.json['size']
        rating = request.json['rating']
        image = request.json['image']

        response = Cupcake.patch(cupcake_id, flavor=flavor, size=size, rating=rating, image=image)

        return jsonify(response)

    elif request.method == "DELETE":

        response = Cupcake.delete(cupcake_id)

        return jsonify(response)

    else:

        return jsonify(["invalid HTTP Verbage"])
    