from pymongo import MongoClient

from conf import MONGO_HOST, MONGO_PORT
from bson.objectid import ObjectId

class MongoDB:
    def __init__(self):
        client = MongoClient(MONGO_HOST, MONGO_PORT)
        db = client['attendanceTracker']
        self.persons = db['persons']
        self.cameras = db['cameras']
        self.tracks = db['tracks']
        self.images = db['images']
    
    def get_persons(self):
        persons = self.persons.find({})
        result = []
        for person in persons:
            person['_id'] = str(person['_id'])
            person['id'] = person.pop('_id')
            result.append(person)
        return result

    def get_cameras(self):
        cameras = self.cameras.find({})
        result = []
        for camera in cameras:
            camera['_id'] = str(camera['_id'])
            camera['id'] = camera.pop('_id')
            result.append(camera)
        return result

    def get_tracks(self):
        tracks = self.tracks.find({})
        result = []
        for track in tracks:
            track['_id'] = str(track['_id'])
            track['id'] = track.pop('_id')
            result.append(track)
        return result
    
    def get_tracks_for_person(self, person_id):
        tracks = self.tracks.find({'person_id': person_id})
        result = []
        for track in tracks:
            track['_id'] = str(track['_id'])
            track['id'] = track.pop('_id')
            result.append(track)
        return result

    def get_tracks_for_camera(self, camera_id):
        trakcs = self.tracks.find({'camera_id': camera_id})
        result = []
        for track in tracks:
            track['_id'] = str(track['_id'])
            track['id'] = track.pop('_id')
            result.append(track)
        return result

    def get_person(self, id):
        person = self.persons.find_one({'_id': ObjectId(id)})
        person['_id'] = str(person['_id'])
        person['id'] = person.pop('_id')
        # print(person)
        return person

    def get_camera(self, id):
        camera = self.cameras.find_one({'_id': ObjectId(id)})
        camera['_id'] = str(camera['_id'])
        camera['id'] = camera.pop('_id')
        return camera

    def get_track(self, id):
        track = self.tracks.find_one({'_id': id})
        track['_id'] = str(track['_id'])
        track['id'] = track.pop('_id')
        return track

    def get_images_for_person(self, person_id):
        images = self.images.find({'personId': person_id})
        result = []
        for image in images:
            result.append(str(image['_id']))
        return result

    def get_all_person_images(self):
        images = self.images.aggregate([
            {
            "$group":
                {
                "_id": "$personId",
                "images": { "$first": "$_id" }
                }
            }
        ])
        result = {}
        for image in images:
            result[str(image['_id'])]= 'http://127.0.0.1:5000/static/images/' + str(image['images'])
        return result

    def add_person(self, person):
        self.persons.insert_one({
            'firstName': person.first_name,
            'lastName': person.last_name,
            'age': person.age,
            'height': person.height,
            'description': person.description
        })

    def add_camera(self, camera):
        self.cameras.insert_one({
            'name': camera.name,
            'ip': camera.ip,
            'port': camera.port
        })

    def add_track(self, track):
        pass

    def add_image(self, person_id):
        _id = self.images.insert_one({
            'personId': person_id,
        }).inserted_id
        return str(_id)

    def edit_person(self, person):
        query = {'_id': ObjectId(person.id)}
        new_values = {
            '$set': {
                'firstName': person.first_name,
                'lastName': person.last_name,
                'age': person.age,
                'height': person.height,
                'description': person.description
            }
        }

        self.persons.update_one(query, new_values)

    def edit_camera(self, camera):
        query = {'_id': ObjectId(camera.id)}
        new_values = {
            '$set': {
                'name': camera.name,
                'ip': camera.ip,
                'port': camera.port
            }
        }

        self.cameras.update_one(query, new_values)


    def edit_track(self, track):
        pass


    def delete_person(self, id):
        query = {'_id': ObjectId(id)}
        self.persons.delete_one(query)

    def delete_camera(self, id):
        query = {'_id': ObjectId(id)}
        self.cameras.delete_one(query)

    def delete_track(self, id):
        query = {'_id': ObjectId(id)}
        self.tracks.delete_one(query)
    
    def delete_image(self, id):
        query = {'_id': ObjectId(id)}
        self.images.delete_one(query)
