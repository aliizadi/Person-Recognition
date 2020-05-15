import threading
import time

import cv2
import jdatetime
import numpy as np
from imutils import paths
from videos_tracker.algorithms import (encode_face, find_unique_faces,
                                       recognize_faces)


NUMBER_OF_FRAMES_MOTION_FINISHED = 50

class Cameras:
    def __init__(self, db):
        self.db = db
        cameras = db.get_cameras()
        self.streams = [Stream(camera, self.db) for camera in cameras]
        for stream in self.streams:
            stream.start()


    def add(self, camera):
        self.streams.append(Stream(camera, self.db))
        self.streams[-1].start()


class Stream(threading.Thread):
    def __init__(self, camera, db):
        threading.Thread.__init__(self)
        self.ip = camera['ip']
        self.port = camera['port']
        self.id = camera['id']
        self.face_encodings = []
        self.frames = []
        self.db = db

    def run(self):

        # cap = cv2.VideoCapture(f'http://{self.ip}:{self.port}/video')
        # cap = cv2.VideoCapture(0)
        cap = Simulation()

        def time_out(x):
            start = 0 
            while start < x:
                _, frame = cap.read()
                start += 1
        
        time_out(0)    

        _, frame = cap.read()
        last_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        last_image = cv2.GaussianBlur(last_image, (21, 21), 0)

        motion_finished = 0
        motion_detected = False

        while True:
            print('capturing frame', motion_finished, motion_detected, cap.index)
            _, frame = cap.read()

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            jalali_datetime = jdatetime.datetime.now()
            date = jalali_datetime.strftime("%a, %d %b %Y")
            time = jalali_datetime.strftime("%H:%M:%S")
            
            current_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            current_image = cv2.GaussianBlur(current_image, (21, 21), 0) 

            diff_frame = cv2.absdiff(last_image, current_image) 
            thresh_frame = cv2.threshold(diff_frame, 70, 255, cv2.THRESH_BINARY)[1]

            last_image = current_image

            if (motion_finished > NUMBER_OF_FRAMES_MOTION_FINISHED and motion_detected):

                motion_detected = False
                motion_finished = 0

                if not self.face_encodings:
                    continue

                print('start_encoding')
                known_persons_encodings = self.db.get_encodings()

                centers_indices, _ = find_unique_faces(self.face_encodings)
                unknown_persons_encodings = [self.face_encodings[i] for i in centers_indices]
                unknown_persons_faces = [self.frames[i] for i in centers_indices]

                found_persons = recognize_faces([encoding['encoding'] for encoding in known_persons_encodings], unknown_persons_encodings)

                self.__add_track(found_persons, unknown_persons_encodings, unknown_persons_faces, known_persons_encodings, date, time)

                self.face_encodings = []
                self.frames = []

            # if there is no difference between current and last frame: skip
            if np.any(thresh_frame):
                motion_detected = True
                motion_finished = 0
                faces = encode_face(frame)
                self.face_encodings.extend([face_encoding[1] for face_encoding in faces])
                self.frames.extend([frame[face_location[0][0]:face_location[0][2], face_location[0][3]:face_location[0][1]] for face_location in faces])

            else:
                motion_finished += 1
                continue

        # cap.release()
        cv2.destroyAllWindows()

    def __add_track(self, found_persons, unknown_persons_encodings, unknown_persons_faces, known_persons_encodings, date, time):

        def new_person(found_person):
            return found_person == -1

        for i, found_person in enumerate(found_persons):
            encoding = unknown_persons_encodings[i].tolist()
            if new_person(found_person):
                print('new person')
                encoding_id = self.db.add_encoding(encoding, self.id)
                track_id = self.db.add_track(encoding_id, self.id, date, time)
                image_id = self.db.add_image(encoding_id, track_id)
                self.__save_image(unknown_persons_faces[i], image_id)
            
            else:
                print('old person')
                encoding_id = known_persons_encodings[found_person]['id']
                self.db.update_encoding(encoding_id, encoding)
                track_id = self.db.add_track(encoding_id, self.id, date, time)
                image_id = self.db.add_image(encoding_id, track_id)
                self.__save_image(unknown_persons_faces[i], image_id)

    
    def __save_image(self, frame, image_id):
        print('trying to save image')
        cv2.imwrite(f'static/images/{image_id}.png', frame)
        print('image saved')


class Simulation:
    def __init__(self):
        self.image_paths = sorted(list(paths.list_images('/home/Person-Recognition/person-recognition/static/dataset/P1L_S1_C1.1')))
        print(len(self.image_paths))
        self.index = 0 

    def read(self):
        frame = cv2.imread(self.image_paths[self.index])
        self.index += 1
        time.sleep(0.05)
        return None, frame
