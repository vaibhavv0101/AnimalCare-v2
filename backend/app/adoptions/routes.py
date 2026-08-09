from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.adoptions import adoptions_bp
from app.adoptions.schemas import AdoptionSchema
from app.adoptions.service import (
    create_adoption,
    get_all_adoptions,
    get_adoption_by_id,
    approve_adoption,
    reject_adoption,
    delete_adoption
)

schema = AdoptionSchema()


@adoptions_bp.route("/", methods=["POST"])
@jwt_required()
def apply_for_adoption():

    errors = schema.validate(request.json)

    if errors:
        return jsonify(errors), 400

    adoption = create_adoption(request.json)

    return jsonify({
        "success": True,
        "message": "Adoption application submitted successfully",
        "adoption_id": adoption.id
    }), 201


@adoptions_bp.route("/", methods=["GET"])
@jwt_required()
def list_adoptions():

    adoptions = get_all_adoptions()

    result = []

    for adoption in adoptions:

        result.append({
            "id": adoption.id,
            "animal_id": adoption.animal_id,
            "user_id": adoption.user_id,
            "reason": adoption.reason,
            "phone": adoption.phone,
            "address": adoption.address,
            "occupation": adoption.occupation,
            "status": adoption.status,
            "created_at": adoption.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        })


    return jsonify({
        "success": True,
        "count": len(result),
        "adoptions": result
    }), 200
    
@adoptions_bp.route("/<int:adoption_id>", methods=["GET"])
@jwt_required()
def adoption_details(adoption_id):

    adoption = get_adoption_by_id(adoption_id)

    if adoption is None:
        return jsonify({
            "success": False,
            "message": "Adoption application not found"
        }), 404

    return jsonify({
        "success": True,
        "adoption": {
            "id": adoption.id,
            "animal_id": adoption.animal_id,
            "user_id": adoption.user_id,
            "reason": adoption.reason,
            "phone": adoption.phone,
            "address": adoption.address,
            "occupation": adoption.occupation,
            "status": adoption.status,
            "created_at": adoption.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    }), 200
    
@adoptions_bp.route(
    "/<int:adoption_id>/approve",
    methods=["PUT"]
)
@jwt_required()
def approve_adoption_application(adoption_id):

    adoption = approve_adoption(adoption_id)

    if adoption is None:
        return jsonify({
            "success": False,
            "message": "Adoption application not found"
        }), 404

    if adoption is False:
        return jsonify({
            "success": False,
            "message": "Animal not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Adoption approved successfully",
        "adoption_id": adoption.id,
        "status": adoption.status
    }), 200
    
@adoptions_bp.route(
    "/<int:adoption_id>/reject",
    methods=["PUT"]
)
@jwt_required()
def reject_adoption_application(adoption_id):

    adoption = reject_adoption(adoption_id)

    if adoption is None:
        return jsonify({
            "success": False,
            "message": "Adoption application not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Adoption rejected successfully",
        "adoption_id": adoption.id,
        "status": adoption.status
    }), 200
    
@adoptions_bp.route(
    "/<int:adoption_id>",
    methods=["DELETE"]
)
@jwt_required()
def remove_adoption(adoption_id):

    deleted = delete_adoption(adoption_id)

    if not deleted:
        return jsonify({
            "success": False,
            "message": "Adoption application not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Adoption application deleted successfully"
    }), 200