from flask import Blueprint, jsonify, request
from app import db
from app.models.planet import Planet

# class Planet: 
#     def __init__(self, id, name, description, position):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.position = position


# planets = [
#     Planet(1, "Mercury", "gray and small", 1),
#     Planet(2, "Venus", "gold and large", 2),
#     Planet(3, "Earth", "greenish and blueish and largish", 3)
# ]


planet_bp = Blueprint( "planet_bp", __name__, url_prefix="/planet")

@planet_bp.route("", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    response = []
    for planet in planets:
        planet_dict = {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "position": planet.position
        }
        response.append(planet_dict)

    return jsonify(response), 200

    

@planet_bp.route("/<planet_id>", methods=["GET"])
def get_specific_planet(planet_id):

    planets = Planet.query.filter_by(id = planet_id )
    try:
        verified_id = int(planet_id)
    except ValueError:
        return jsonify("invalid ID. ID must be an integer"), 400

    for planet in planets:
        if planet.id == verified_id:
            planet_dict = {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "position": planet.position
            }
            return jsonify(planet_dict), 200
    return jsonify(f"ID: '{verified_id}' not found"), 404

    


@planet_bp.route("", methods=["POST"])
def add_planet():
    request_body = request.get_json()

    new_planet = Planet(
            name = request_body["name"],
            description = request_body["description"],
            position = request_body["position"]
    )

    db.session.add(new_planet)
    db.session.commit()

    return {"id": new_planet.id}, 201