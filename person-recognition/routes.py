from flask import Flask, request, make_response, jsonify, abort, send_from_directory, redirect, url_for
from db import MongoDB 
from models import Camera, Person, Track
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/images'

db = MongoDB()

@app.route('/api')
def index():
    return "Attendance Tracker" 

@app.route('/api/persons', methods=['GET'])
def get_persons():
    return jsonify({'persons': db.get_persons()})
    
@app.route('/api/cameras', methods=['GET'])
def get_cameras():
    return jsonify({'cameras': db.get_cameras()})

@app.route('/api/tracks', methods=['GET'])
def get_tracks():
    return jsonify({'tracks': db.get_tracks()})

@app.route('/api/persons/profile/<string:id>', methods=['GET'])
def get_person(id):
    person = db.get_person(id)
    return jsonify({'person': person})

@app.route('/api/persons/tracks/<string:id>', methods=['GET'])
def get_tracks_for_person(id):
    tracks = db.get_tracks_for_person(id)
    return jsonify({'tracks': tracks})

@app.route('/api/persons/images/<string:id>', methods=['GET'])
def get_images_for_person(id):
    images = db.get_images_for_person(id)
    images_list = [{'img': str(image)} for image in images]
    # print(images_list)
    return jsonify({'images': images_list})

@app.route('/api/persons/all/images', methods=['GET'])
def get_all_person_images():
    images = db.get_all_person_images()
    return jsonify({'images': images})
    
@app.route('/api/cameras/inf/<string:id>', methods=['GET'])
def get_camera(id):
    camera = db.get_camera(id)
    return jsonify({'camera': camera})

@app.route('/api/cameras/tracks/<string:id>', methods=['GET'])
def get_tracks_for_camera(id):
    tracks = db.get_tracks_for_camera(id)

    return jsonify({'tracks': tracks})
    
## if need to handle other query parameters follow this link part Improving the web service interface
## https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
## also follow above link for implementing authentication

@app.route('/api/tracks/<string:id>', methods=['GET'])
def get_track(id):
    track = db.get_track(id)
    return jsonify({'track': track})

@app.route('/api/persons', methods=['POST'])
def add_person():

    person = Person(
        id=-1,
        first_name=request.json['firstName'],
        last_name=request.json['lastName'],
        age=request.json['age'],
        height=request.json['height'],
        description=request.json['description'],
    )

    db.add_person(person)
    return jsonify({'person': 'true'}), 201

@app.route('/api/cameras', methods=['POST'])
def add_camera():

    camera = Camera(
        id=-1,
        name=request.json['name'],
        ip=request.json['ip'],
        port=request.json['port'],
    )

    db.add_camera(camera)
    return jsonify({'camera': 'true'}), 201
        
# @app.route('/api/tracks', methods=['POST'])
# def add_track():
#     abort(400)

# ALLOWED_EXTENSIONS = {'png', 'jpg'}

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/api/persons/images/<string:id>', methods=['POST'])
# def add_image(id):
#     if 'file' not in request.files:
#         print('no file in request')
#         return ""

#     file = request.files['file']

#     if file.filename == '':
#         print('no selected file')
#         return ""

#     if file and allowed_file(file.filename):
        
#         file_name_id = db.add_image(id)
#         print(file_name_id)
#         filename = secure_filename(file_name_id)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return ""

#     return jsonify({'image': 'true'})

@app.route('/api/persons', methods=['PUT'])
def edit_person():

    person = db.get_person(request.json['id'])

    edited_person = Person(
    id=person['id'],
    first_name=request.json['firstName'],
    last_name=request.json['lastName'],
    age=request.json['age'],
    height=request.json['height'],
    description=request.json['description'],
    )

    result = db.edit_person(edited_person)

    return jsonify({'person': 'true'})

@app.route('/api/cameras', methods=['PUT'])
def edit_camera():

    camera = db.get_camera(request.json['id'])

    edited_camera = Camera(
        id=camera['id'],
        name=request.json['name'],
        ip=request.json['ip'],
        port=request.json['port'],
    )

    db.edit_camera(edited_camera)

    return jsonify({'camera': 'true'})

@app.route('/api/tracks', methods=['PUT'])
def edit_track():
    track = db.get_track(request.json['id'])
    edited_track = Track(
        id=track['id'],
        date = track['date'],
        time = track['time'],
        kind = track['kind'],
        camera_id = track['camera']['id'],
        person_id = request.json['person']['id'],
        encoding_id = request.json['encoding_id'],
        image = track['image']
    )

    db.edit_track(edited_track)

    return jsonify({'track': 'true'})

@app.route('/api/persons/<string:id>', methods=['DELETE'])
def delete_person(id):
    
    person = db.get_person(id)
    db.delete_person(person['id'])

    return jsonify({'result': True})

@app.route('/api/cameras/<string:id>', methods=['DELETE'])
def delete_camera(id):
    
    camera = db.get_camera(id)        
    db.delete_camera(camera['id'])
    
    return jsonify({'result': True})

@app.route('/api/tracks/<string:id>', methods=['DELETE'])
def delete_track(id):
    
    track = db.get_track(id)
    db.delete_track(track['id'])
    
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./static', path)

 
if __name__ == '__main__':
    app.run(debug=True)
