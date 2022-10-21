from flask import Blueprint, jsonify

class Planet: 
    def __init__(self, id, name, description, position):
        self.id = id
        self.name = name
        self.description = description
        self.position = position


planets = [
    Planet(1, "Mercury", "gray and small", 1),
    Planet(2, "Venus", "gold and large", 2),
    Planet(3, "Earth", "greenish and blueish and largish", 3)
]


planet_bp = Blueprint( "planet_bp", __name__, url_prefix="/planets")

@planet_bp.route("", methods=["GET"])
def get_planets():
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
    try:
        varified_id = int(planet_id)
    except ValueError:
        return jsonify("invalid ID. ID must be an integer"), 400

    for planet in planets:
        if planet.id == varified_id:
            planet_dict = {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "position": planet.position
            }
            return jsonify(planet_dict), 200
    return jsonify(f"ID: '{varified_id}' not found"), 404