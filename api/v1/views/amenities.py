#!/usr/bin/python3
"""States cities ect..
"""
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """
    Retrieves all the amenities list objects
    """
    Amenity_List = []
    for key, value in storage.all(Amenity).items():
        Amenity_List.append(value.to_dict())
    return jsonify(Amenity_List)

@app_views.route('/amenities/<amenities_id>', strict_slashes=False)
def get_amenities(amenities_id):
    """
    Retrieves a Amenity object
    """
    amenities = storage.get(Amenity, amenities_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)

@app_views.route('/amenities/<amenities_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenities(amenities_id):
    """
    Deletes a Amenity object
    """
    amenity = storage.get(Amenity, amenities_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)

@app_views.route('/amenities', methods=['post'], strict_slashes=False)
def create_amenities(amenities_id):
    """
    Retrieves a Amenity object
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    
    if 'name' not in data:
        return abort(400, 'Missing name')
    
    amenity = Amenity(**data)
    
    amenity.save()
    
    return jsonify(amenity.to_dict()), 200

@app_views.route('/amenities/amenity_id', methods=['put'], strict_slashes=False)
def update_amenities(amenities_id):
    """
    Retrieves a Amenity object
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()

Amenity = storage.get(Amenity, amenities_id)
if amenity:
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
else:
    abort(404)