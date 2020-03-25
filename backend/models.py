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
    def __init__(self, person, date, time, kind, camera):
        self.person = person
        self.date = date
        self.time = time
        self.kind = kind 
        self.camera = camera
