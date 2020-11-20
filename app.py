"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template, redirect
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretkey"

connect_db(app)

def serialize_cupcake(cupcake):
    """Serialize a cupcake."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

#############################   FLASK ROUTES   #############################

@app.route("/")
def index_page():
    """Render html showing cupcakes"""

    return render_template("index.html")

@app.errorhandler(404)
def error(e):
    """Redirect user to home page on 404 error"""

    return redirect("/")

#################################   API   #################################

@app.route("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>")
def list_one_cupcakes(cupcake_id):
    """Return JSON {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create cupcake and return JSON {cupcake: {id, flavor, size, rating, image}}"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake=serialized), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake and return JSON {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete a cupcake and return JSON {message: "Deleted"}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")