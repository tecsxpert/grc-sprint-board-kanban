from flask import Blueprint, jsonify

report_bp = Blueprint("report", __name__)

@report_bp.route("/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Report route working"})