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
        self.encodings = db['encodings']
    
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

    def __create_track_model(self, track):
        track['camera'] = self.get_camera(track['camera_id'])
        image = self.get_image_for_track(track['id'])
        track['image'] = image

        encoding = self.get_encoding(track['encoding_id'])
        encoding_person_id = encoding['person_id']

        if encoding_person_id:
            track['person'] = self.get_person(encoding_person_id)
        else:
            track['person'] = {
                'id': track['encoding_id'],
                'firstName': 'بدون نام',
                'lastName': 'بدون نام',
                'age': '',
                'height': '',
                'description': ''
             }
        track.pop('camera_id')

        return track 

    def get_tracks(self):
        tracks = self.tracks.find({})
        result = []
        for track in tracks:
            track['_id'] = str(track['_id'])
            track['id'] = track.pop('_id')
            result.append(self.__create_track_model(track))
        return result

    
    def get_tracks_for_person(self, person_id):
        encoding_for_person = self.get_encoding_for_person(person_id)

        if encoding_for_person:
            tracks = self.tracks.find({'encoding_id': encoding_for_person['id']})
            result = []
            for track in tracks:
                track['_id'] = str(track['_id'])
                track['id'] = track.pop('_id')
                result.append(self.__create_track_model(track))
            return result
        
        else:
            return []

    def get_tracks_for_camera(self, camera_id):
        tracks = self.tracks.find({'camera_id': camera_id})
        result = []
        for track in tracks:
            track['_id'] = str(track['_id'])
            track['id'] = track.pop('_id')
            result.append(self.__create_track_model(track))
        return result

    def get_person(self, id):
        person = self.persons.find_one({'_id': ObjectId(id)})
        person['_id'] = str(person['_id'])
        person['id'] = person.pop('_id')
        return person

    def get_camera(self, id):
        camera = self.cameras.find_one({'_id': ObjectId(id)})
        camera['_id'] = str(camera['_id'])
        camera['id'] = camera.pop('_id')
        return camera

    def get_track(self, id):
        track = self.tracks.find_one({'_id': ObjectId(id)})
        track['_id'] = str(track['_id'])
        track['id'] = track.pop('_id')
        return self.__create_track_model(track)

    def get_image_for_track(self, track_id):
        image = self.images.find_one({'track_id': track_id})
        return str(image['_id'])

    def get_images_for_person(self, person_id):
        encoding_for_person = self.get_encoding_for_person(person_id)

        if encoding_for_person:
            images = self.images.find({'encoding_id': encoding_for_person['id']})
            result = []
            for image in images:
                result.append(str(image['_id']))
            return result
        
        else:
            return []

    def get_all_person_images(self):
        images = self.images.aggregate([
            {
            "$group":
                {
                "_id": "$encoding_id",
                "images": { "$first": "$_id" }
                }
            }
        ])
        result = {}
        for image in images:
            encoding = self.get_encoding(str(image['_id']))
            encoding_person_id = encoding['person_id']

            if encoding_person_id:
                result[encoding_person_id]= str(image['images'])
            else:
                continue
            
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

    def add_track(self, encoding_id, camera_id, date, time):
        _id = self.tracks.insert_one({
            'encoding_id': encoding_id,
            'camera_id': camera_id,
            'kind': 'ورود',
            'time': time,
            'date': date
        }).inserted_id
        return str(_id)

    def add_image(self, encoding_id, track_id):
        _id = self.images.insert_one({
            'encoding_id': encoding_id,
            'track_id': track_id

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
        query = {'_id': ObjectId(track.id)}
        encoding_for_person = self.get_encoding_for_person(track.person_id)
        if encoding_for_person:
            self.edit_encoding(encoding_for_person['id'], track.person_id)
        else:
            self.edit_encoding(track.encoding_id, track.person_id)


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


    def get_encodings(self):
        encodings = self.encodings.find({})
        result = []
        for encoding in encodings:
            encoding['_id'] = str(encoding['_id'])
            encoding['id'] = encoding.pop('_id')
            result.append(encoding)
        return result

    def get_encoding(self, id):
        encoding = self.encodings.find_one({'_id': ObjectId(id)})
        encoding['_id'] = str(encoding['_id'])
        encoding['id'] = encoding.pop('_id')
        return encoding

    def get_encoding_for_person(self, person_id):
        encoding = self.encodings.find_one({'person_id': person_id})
        if encoding:
            encoding['_id'] = str(encoding['_id'])
            encoding['id'] = encoding.pop('_id')
            return encoding
        else:
            return None
    
    def add_encoding(self, encoding, camera_id):
        _id = self.encodings.insert_one({
            'encoding': encoding,
            'person_id': None,
            'camera_id': camera_id
        }).inserted_id
        return str(_id)

    def edit_encoding(self, encoding_id, person_id):
        query = {'_id': ObjectId(encoding_id)}
        new_values = {
            '$set': {
                'person_id': person_id,
            }
        }
        self.encodings.update_one(query, new_values)

    def update_encoding(self, encoding_id, encoding):
        query = {'_id': ObjectId(encoding_id)}
        new_values = {
            '$set': {
                'encoding': encoding,
            }
        }
        self.encodings.update_one(query, new_values)
