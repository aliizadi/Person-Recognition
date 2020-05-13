class Person:
    def __init__(self, id, first_name, last_name, age, height, description):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.height = height
        self.description = description

class Camera:
    def __init__(self, id, name, ip, port):
        self.id = id 
        self.name = name
        self.ip = ip
        self.port = port

class Track:
    def __init__(self, id, person_id, date, time, kind, camera_id, encoding_id, image):
        self.id = id
        self.person_id = person_id
        self.date = date
        self.time = time
        self.kind = kind 
        self.camera_id = camera_id
        self.encoding_id = encoding_id
        self.image = image
