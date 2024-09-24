from . import app
import os
import json
from flask import Response, jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    search_result = None
    for record in data:
        if record["id"] == id:
            search_result = record
            break
    if search_result is None:
        return {"message": "not found"}, 404
    return jsonify(search_result)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    json_record = json.loads(request.data)
    search_result = None
    for record in data:
        if record["id"] == json_record["id"]:
            search_result = record
            break
    if search_result is not None:
        return {"Message": f"picture with id {json_record['id']} already present"}, 302
    data.append(json_record)
    return json_record, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    json_record = json.loads(request.data)
    search_result = None
    for index,record in enumerate(data):
        if record["id"] == id:
            search_result = record
            data[index] = json_record
            break
    if search_result is None:
        return {"message": "picture not found"}, 404
    return "updated"

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    search_result = None
    for index,record in enumerate(data):
        if record["id"] == id:
            search_result = record
            del(data[index])
            break
    if search_result is None:
        return {"message": "picture not found"}, 404
    return Response(status=204)
