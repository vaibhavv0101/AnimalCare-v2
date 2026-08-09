from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.ngos import ngos_bp
from app.ngos.schemas import NGOSchema
from app.ngos.service import (
    create_ngo,
    get_all_ngos,
    get_ngo_by_id,
    update_ngo,
    delete_ngo
)

schema = NGOSchema()


@ngos_bp.route("/", methods=["POST"])
@jwt_required()
def add_ngo():

    errors = schema.validate(request.json)

    if errors:
        return jsonify(errors), 400

    ngo = create_ngo(request.json)

    return jsonify({
        "success": True,
        "message": "NGO registered successfully",
        "ngo_id": ngo.id
    }), 201
    
@ngos_bp.route("/", methods=["GET"])
@jwt_required()
def list_ngos():

    ngos = get_all_ngos()

    result = []

    for ngo in ngos:

        result.append({
            "id": ngo.id,
            "name": ngo.name,
            "email": ngo.email,
            "phone": ngo.phone,
            "address": ngo.address,
            "registration_number": ngo.registration_number,
            "description": ngo.description,
            "status": ngo.status,
            "created_at": ngo.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        })

    return jsonify({
        "success": True,
        "count": len(result),
        "ngos": result
    }), 200

@ngos_bp.route("/<int:ngo_id>", methods=["GET"])
@jwt_required()
def ngo_details(ngo_id):

    ngo = get_ngo_by_id(ngo_id)

    if ngo is None:
        return jsonify({
            "success": False,
            "message": "NGO not found"
        }), 404

    return jsonify({
        "success": True,
        "ngo": {
            "id": ngo.id,
            "name": ngo.name,
            "email": ngo.email,
            "phone": ngo.phone,
            "address": ngo.address,
            "registration_number": ngo.registration_number,
            "description": ngo.description,
            "status": ngo.status,
            "created_at": ngo.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    }), 200
    
@ngos_bp.route("/<int:ngo_id>", methods=["PUT"])
@jwt_required()
def edit_ngo(ngo_id):

    if not request.json:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    ngo = update_ngo(ngo_id, request.json)

    if ngo is None:
        return jsonify({
            "success": False,
            "message": "NGO not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "NGO updated successfully",
        "ngo": {
            "id": ngo.id,
            "name": ngo.name,
            "email": ngo.email,
            "phone": ngo.phone,
            "address": ngo.address,
            "registration_number": ngo.registration_number,
            "description": ngo.description,
            "status": ngo.status
        }
    }), 200
    
@ngos_bp.route("/<int:ngo_id>", methods=["DELETE"])
@jwt_required()
def remove_ngo(ngo_id):

    deleted = delete_ngo(ngo_id)

    if not deleted:
        return jsonify({
            "success": False,
            "message": "NGO not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "NGO deleted successfully"
    }), 200