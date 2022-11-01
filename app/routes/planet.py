from flask import Blueprint, jsonify, request, abort, make_response
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
    name_param = request.args.get("name")
    description_param = request.args.get("description")
    position_param = int(request.args.get("position"))

    planets = Planet.query.all()
    
    if name_param is None and \
    description_param is None and \
    position_param is None:
        pass
    else:
        if name_param:
            planets = [x for x in planets if x.name == name_param]
        if description_param:
            planets = [x for x in planets if x.description == description_param]
        if position_param:
            planets = [x for x in planets if int(x.position) == position_param]

    
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



def get_one_planet_or_abort(planet_id):
    try:
        verified_id = int(planet_id)
    except ValueError:
        abort(make_response(jsonify("invalid ID. ID must be an integer"), 400))

    planet = Planet.query.get(planet_id)

    if planet is None:
        response_str = f"Planet with #{planet_id} was not found in the database"
        abort(make_response(jsonify("invalid ID. ID was not found"), 404))

    return planet


@planet_bp.route("/<planet_id>", methods=["GET"])
def get_specific_planet(planet_id):
    planet = get_one_planet_or_abort(planet_id)

    planet_dict = {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "position": planet.position
    }
    
    return jsonify(planet_dict), 200


@planet_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = get_one_planet_or_abort(planet_id)

    request_body = request.get_json()

    if "name" not in request_body \
    or "description" not in request_body \
    or "position" not in request_body:
        return jsonify({"message": "Request must include: name, description, position"})

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.position = request_body["position"]
            
    db.session.commit()

    return jsonify({"message":f"Successfully replaced planet with planet id: {planet_id}"}), 200


@planet_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = get_one_planet_or_abort(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message":f"Successfully deleted planet with planet id: {planet_id}"}), 200
