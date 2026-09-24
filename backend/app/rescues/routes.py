from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.rescues import rescues_bp

from app.rescues.schemas import RescueSchema

from app.rescues.service import (
    create_rescue,
    get_all_rescues,
    get_my_rescues,
    get_rescue_by_id,
    update_rescue_status,
    assign_ngo,
    assign_volunteer,
    delete_rescue
    
)

from app.auth.decorators import role_required
from app.models.ngo import NGO
from app.models.volunteer import Volunteer

schema = RescueSchema()


# ============================================================
# CREATE RESCUE
# ============================================================

@rescues_bp.route("/", methods=["POST"])
@jwt_required()
def add_rescue():

    errors = schema.validate(request.json)

    if errors:

        return jsonify(errors), 400

    rescue = create_rescue(request.json)

    if rescue is None:

        return jsonify({

            "success": False,

            "message": "Animal not found"

        }), 404

    return jsonify({

        "success": True,

        "message": "Rescue request created successfully",

        "rescue_id": rescue.id

    }), 201
# ============================================================
# GET MY RESCUE REQUESTS
# NORMAL LOGGED-IN USER
# ============================================================

@rescues_bp.route("/my", methods=["GET"])
@jwt_required()
def my_rescue_requests():

    rescues = get_my_rescues()

    result = []

    for rescue in rescues:
     ngo = NGO.query.get(rescue.assigned_ngo) if rescue.assigned_ngo else None
    volunteer = Volunteer.query.get(rescue.assigned_volunteer) if rescue.assigned_volunteer else None
    result.append({
            "id": rescue.id,
            "animal_id": rescue.animal_id,
            "reported_by": rescue.reported_by,
            "assigned_ngo": rescue.assigned_ngo,
            "assigned_volunteer": rescue.assigned_volunteer,
            "ngo_name": ngo.name if ngo else None,
"volunteer_name": volunteer.name if volunteer else None,
"ngo_phone": ngo.phone if ngo else None,
"ngo_email": ngo.email if ngo else None,
"volunteer_phone": volunteer.phone if volunteer else None,
"volunteer_email": volunteer.email if volunteer else None,
            "latitude": rescue.latitude,
            "longitude": rescue.longitude,
            "address": rescue.address,
            "priority": rescue.priority,
            "status": rescue.status,
            "notes": rescue.notes,
            "created_at": (
                rescue.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if rescue.created_at
                else None
            )
        })

    return jsonify({
        "success": True,
        "count": len(result),
        "rescues": result
    }), 200

# ============================================================
# GET ALL RESCUES
# ============================================================

@rescues_bp.route("/", methods=["GET"])
@jwt_required()
def list_rescues():

    rescues = get_all_rescues()

    result = []

    for rescue in rescues:

     result.append({
            "id": rescue.id,

            "animal_id": rescue.animal_id,

            "reported_by": rescue.reported_by,

            "assigned_ngo": rescue.assigned_ngo,

            "assigned_volunteer": rescue.assigned_volunteer,

            "latitude": rescue.latitude,

            "longitude": rescue.longitude,

            "address": rescue.address,

            "priority": rescue.priority,

            "status": rescue.status,

            "notes": rescue.notes,

            "created_at": (
                rescue.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if rescue.created_at
                else None
            )

        })

    return jsonify({

        "success": True,

        "count": len(result),

        "rescues": result

    }), 200


# ============================================================
# GET SINGLE RESCUE
# ============================================================

@rescues_bp.route(
    "/<int:rescue_id>",
    methods=["GET"]
)
@jwt_required()
def rescue_details(rescue_id):

    rescue = get_rescue_by_id(rescue_id)

    if rescue is None:

        return jsonify({

            "success": False,

            "message": "Rescue not found"

        }), 404

    return jsonify({

        "success": True,

        "rescue": {

            "id": rescue.id,

            "animal_id": rescue.animal_id,

            "reported_by": rescue.reported_by,

            "assigned_ngo": rescue.assigned_ngo,

            "assigned_volunteer": rescue.assigned_volunteer,

            "latitude": rescue.latitude,

            "longitude": rescue.longitude,

            "address": rescue.address,

            "priority": rescue.priority,

            "status": rescue.status,

            "notes": rescue.notes,

            "created_at": (
                rescue.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if rescue.created_at
                else None
            )

        }

    }), 200


# ============================================================
# UPDATE RESCUE STATUS
# ADMIN ONLY
# ============================================================

@rescues_bp.route(
    "/<int:rescue_id>/status",
    methods=["PUT"]
)
@jwt_required()
@role_required("Admin")
def change_status(rescue_id):

    if (
        not request.json
        or "status" not in request.json
    ):

        return jsonify({

            "success": False,

            "message": "Status is required"

        }), 400

    rescue = update_rescue_status(
        rescue_id,
        request.json
    )

    if rescue is None:

        return jsonify({

            "success": False,

            "message": "Rescue not found"

        }), 404

    return jsonify({

        "success": True,

        "message": "Rescue status updated successfully",

        "status": rescue.status

    }), 200


# ============================================================
# ASSIGN NGO
# ADMIN ONLY
# ============================================================

@rescues_bp.route(
    "/<int:rescue_id>/assign-ngo",
    methods=["PUT"]
)
@jwt_required()
@role_required("Admin")
def assign_ngo_route(rescue_id):

    if (
        not request.json
        or "ngo_id" not in request.json
    ):

        return jsonify({

            "success": False,

            "message": "ngo_id is required"

        }), 400

    rescue = assign_ngo(
        rescue_id,
        request.json["ngo_id"]
    )

    if rescue is None:

        return jsonify({

            "success": False,

            "message": "Rescue not found"

        }), 404

    if rescue is False:

        return jsonify({

            "success": False,

            "message": "NGO not found"

        }), 404

    return jsonify({

        "success": True,

        "message": "NGO assigned successfully",

        "assigned_ngo": rescue.assigned_ngo

    }), 200


# ============================================================
# ASSIGN VOLUNTEER
# ADMIN ONLY
# ============================================================

@rescues_bp.route(
    "/<int:rescue_id>/assign-volunteer",
    methods=["PUT"]
)
@jwt_required()
@role_required("Admin")
def assign_volunteer_route(rescue_id):

    if (
        not request.json
        or "volunteer_id" not in request.json
    ):

        return jsonify({

            "success": False,

            "message": "volunteer_id is required"

        }), 400

    rescue = assign_volunteer(
        rescue_id,
        request.json["volunteer_id"]
    )

    if rescue is None:

        return jsonify({

            "success": False,

            "message": "Rescue not found"

        }), 404

    if rescue is False:

        return jsonify({

            "success": False,

            "message": "Volunteer not found"

        }), 404

    return jsonify({

        "success": True,

        "message": "Volunteer assigned successfully",

        "assigned_volunteer":
            rescue.assigned_volunteer

    }), 200


# ============================================================
# DELETE RESCUE
# ADMIN ONLY
# ============================================================

@rescues_bp.route(
    "/<int:rescue_id>",
    methods=["DELETE"]
)
@jwt_required()
@role_required("Admin")
def remove_rescue(rescue_id):

    deleted = delete_rescue(rescue_id)

    if not deleted:

        return jsonify({

            "success": False,

            "message": "Rescue not found"

        }), 404

    return jsonify({

        "success": True,

        "message": "Rescue deleted successfully"

    }), 200