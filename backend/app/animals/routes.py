from flask import request, jsonify

from flask_jwt_extended import jwt_required

from app.animals import animals_bp
from app.animals.schemas import AnimalSchema

from app.models.animal import Animal

from app.animals.service import (
    create_animal,
    get_all_animals,
    get_animal_by_id,
    update_animal,
    delete_animal
)

schema = AnimalSchema()


@animals_bp.route("/", methods=["POST"])
@jwt_required()
def add_animal():

    errors = schema.validate(request.json)

    if errors:
        return jsonify(errors), 400

    animal = create_animal(request.json)

    return jsonify({
        "success": True,
        "message": "Animal added successfully",
        "animal_id": animal.id
    }), 201
    
@animals_bp.route("/", methods=["GET"])
@jwt_required()
def list_animals():

    animals = get_all_animals()

    result = []

    for animal in animals:

        result.append({
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,
            "breed": animal.breed,
            "gender": animal.gender,
            "age": animal.age,
            "color": animal.color,
            "weight": animal.weight,
            "health_status": animal.health_status,
            "adoption_status": animal.adoption_status
        })

    return jsonify({
        "success": True,
        "count": len(result),
        "animals": result
    })
    
@animals_bp.route("/<int:animal_id>", methods=["GET"])
@jwt_required()
def animal_details(animal_id):

    animal = get_animal_by_id(animal_id)

    if animal is None:
        return jsonify({
            "success": False,
            "message": "Animal not found"
        }), 404

    return jsonify({
        "success": True,
        "animal": {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,
            "breed": animal.breed,
            "gender": animal.gender,
            "age": animal.age,
            "color": animal.color,
            "weight": animal.weight,
            "rescue_location": animal.rescue_location,
            "health_status": animal.health_status,
            "vaccination_status": animal.vaccination_status,
            "description": animal.description,
            "adoption_status": animal.adoption_status
        }
    })
    
@animals_bp.route("/<int:animal_id>", methods=["PUT"])
@jwt_required()
def edit_animal(animal_id):

    errors = schema.validate(request.json, partial=True)

    if errors:
        return jsonify(errors), 400

    animal = update_animal(animal_id, request.json)

    if animal is None:
        return jsonify({
            "success": False,
            "message": "Animal not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Animal updated successfully"
    }), 200

@animals_bp.route("/<int:animal_id>", methods=["DELETE"])
@jwt_required()
def remove_animal(animal_id):

    deleted = delete_animal(animal_id)

    if not deleted:
        return jsonify({
            "success": False,
            "message": "Animal not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Animal deleted successfully"
    }), 200