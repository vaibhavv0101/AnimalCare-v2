from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.volunteers import volunteers_bp
from app.volunteers.schemas import VolunteerSchema
from app.volunteers.service import (
    create_volunteer,
    get_all_volunteers,
    get_volunteer_by_id,
    update_volunteer,
    delete_volunteer
)

schema = VolunteerSchema()

@volunteers_bp.route("/", methods=["POST"])
@jwt_required()
def add_volunteer():

    errors = schema.validate(request.json)

    if errors:
        return jsonify(errors), 400

    volunteer = create_volunteer(request.json)

    return jsonify({
        "success": True,
        "message": "Volunteer registered successfully",
        "volunteer_id": volunteer.id
    }), 201
    
@volunteers_bp.route("/", methods=["GET"])
@jwt_required()
def list_volunteers():

    volunteers = get_all_volunteers()

    result = []

    for volunteer in volunteers:

        result.append({
            "id": volunteer.id,
            "name": volunteer.name,
            "email": volunteer.email,
            "phone": volunteer.phone,
            "address": volunteer.address,
            "skills": volunteer.skills,
            "availability": volunteer.availability,
            "status": volunteer.status,
            "created_at": volunteer.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        })

    return jsonify({
        "success": True,
        "count": len(result),
        "volunteers": result
    }), 200
    
@volunteers_bp.route("/<int:volunteer_id>", methods=["GET"])
@jwt_required()
def volunteer_details(volunteer_id):

    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer is None:
        return jsonify({
            "success": False,
            "message": "Volunteer not found"
        }), 404

    return jsonify({
        "success": True,
        "volunteer": {
            "id": volunteer.id,
            "name": volunteer.name,
            "email": volunteer.email,
            "phone": volunteer.phone,
            "address": volunteer.address,
            "skills": volunteer.skills,
            "availability": volunteer.availability,
            "status": volunteer.status,
            "created_at": volunteer.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    }), 200
    
@volunteers_bp.route("/<int:volunteer_id>", methods=["PUT"])
@jwt_required()
def edit_volunteer(volunteer_id):

    if not request.json:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    volunteer = update_volunteer(
        volunteer_id,
        request.json
    )

    if volunteer is None:
        return jsonify({
            "success": False,
            "message": "Volunteer not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Volunteer updated successfully",
        "volunteer": {
            "id": volunteer.id,
            "name": volunteer.name,
            "email": volunteer.email,
            "phone": volunteer.phone,
            "address": volunteer.address,
            "skills": volunteer.skills,
            "availability": volunteer.availability,
            "status": volunteer.status
        }
    }), 200
    
@volunteers_bp.route("/<int:volunteer_id>", methods=["DELETE"])
@jwt_required()
def remove_volunteer(volunteer_id):

    deleted = delete_volunteer(volunteer_id)

    if not deleted:
        return jsonify({
            "success": False,
            "message": "Volunteer not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Volunteer deleted successfully"
    }), 200