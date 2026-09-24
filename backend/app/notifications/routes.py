from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.notification import Notification
from app.notifications import notifications_bp


# ============================================================
# GET MY NOTIFICATIONS
# ============================================================

@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def get_my_notifications():

    user_id = int(get_jwt_identity())

    notifications = (
        Notification.query
        .filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return jsonify({
        "success": True,
        "count": len(notifications),
        "notifications": [
            notification.to_dict()
            for notification in notifications
        ]
    }), 200


# ============================================================
# GET UNREAD NOTIFICATION COUNT
# ============================================================

@notifications_bp.route("/unread-count", methods=["GET"])
@jwt_required()
def unread_notification_count():

    user_id = int(get_jwt_identity())

    count = Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).count()

    return jsonify({
        "success": True,
        "unread_count": count
    }), 200


# ============================================================
# MARK ONE NOTIFICATION AS READ
# ============================================================

@notifications_bp.route(
    "/<int:notification_id>/read",
    methods=["PUT"]
)
@jwt_required()
def mark_notification_as_read(notification_id):

    user_id = int(get_jwt_identity())

    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=user_id
    ).first()

    if notification is None:
        return jsonify({
            "success": False,
            "message": "Notification not found"
        }), 404

    notification.is_read = True

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Notification marked as read",
        "notification": notification.to_dict()
    }), 200


# ============================================================
# MARK ALL MY NOTIFICATIONS AS READ
# ============================================================

@notifications_bp.route(
    "/read-all",
    methods=["PUT"]
)
@jwt_required()
def mark_all_notifications_as_read():

    user_id = int(get_jwt_identity())

    notifications = Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).all()

    for notification in notifications:
        notification.is_read = True

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "All notifications marked as read",
        "updated_count": len(notifications)
    }), 200