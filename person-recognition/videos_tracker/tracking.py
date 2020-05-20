import threading
import time

import cv2
import dlib
import jdatetime
import numpy as np
from imutils import paths

from videos_tracker.algorithms import encode_face
from videos_tracker.centroidtracker import CentroidTracker

NUMBER_OF_SKIP_FRAMES_TO_FACE_DETECTION = 1
NUMBER_OF_MAX_FRAMES_FACE_DISAPPEARED=30
MAXIMUM_DISTANCE_BETWEEN_TO_CENTER=50


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

    def __time_out(self, x):
            start = 0 
            while start < x:
                _, frame = cap.read()
                start += 1


    def run(self):

        # cap = cv2.VideoCapture(f'http://{self.ip}:{self.port}/video')
        # cap = cv2.VideoCapture(0)
        cap = Simulation()

        centroid_tracker = CentroidTracker(self.db, camera_id=self.id, max_frames_disappeared=NUMBER_OF_MAX_FRAMES_FACE_DISAPPEARED, max_distance=MAXIMUM_DISTANCE_BETWEEN_TO_CENTER)
        trackers = []

        _, frame = cap.read()

        

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        last_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        last_image = cv2.GaussianBlur(last_image, (21, 21), 0)

        finished = False

        frames_num = 0 
        total_frames = 0

        # TODO check what happend to last elements
        while True:

            frames_num += 1
            total_frames += 1
            print('capturing frames', total_frames)

            finished , frame = cap.read()

            # cv2.imshow('frame', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            jalali_datetime = jdatetime.datetime.now()
            date = jalali_datetime.strftime("%a, %d %b %Y")
            time = jalali_datetime.strftime("%H:%M:%S")
            
            current_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            current_image = cv2.GaussianBlur(current_image, (21, 21), 0) 

            diff_frame = cv2.absdiff(last_image, current_image) 
            thresh_frame = cv2.threshold(diff_frame, 10, 255, cv2.THRESH_BINARY)[1]

            last_image = current_image

            if finished:
                centroid_tracker.update(rects)

            # if there is no difference between current and last frame: skip
            if np.any(thresh_frame):

                rects = []
                if total_frames % NUMBER_OF_SKIP_FRAMES_TO_FACE_DETECTION == 0:
                    trackers = []

                
                    faces = encode_face(frame)

                    # print('object detector - --------------------------------------------------------', len(faces))


                    for face in faces:
                        
                        encoding = face[1]
                        top, right, bottom, left = face[0]
                        
                        tracker = dlib.correlation_tracker()
                        rect = dlib.rectangle(left, top, right, bottom)
                        tracker.start_track(rgb, rect)
                        trackers.append(tracker)
                        rects.append(((left, top, right, bottom), encoding, frame, date, time))
                else:
                    # print('tracker', len(trackers))

                    for tracker in trackers:
                        tracker.update(rgb)
                        pos = tracker.get_position()
                        startX = int(pos.left())
                        startY = int(pos.top())
                        endX = int(pos.right())
                        endY = int(pos.bottom())
                        rects.append(((startX, startY, endX, endY), None , None, None, None))

                

                objects = centroid_tracker.update(rects)

            else:
                # total_frames = 0
                continue

        # cap.release()
        # cv2.destroyAllWindows()

class Simulation:
    def __init__(self):
        self.image_paths = sorted(list(paths.list_images('/home/Person-Recognition/person-recognition/static/dataset/P2E_S1_C3.1')))
        print(len(self.image_paths))
        self.index = 0 

    def read(self):
        try:            
            frame = cv2.imread(self.image_paths[self.index])
            self.index += 1
            time.sleep(0.05)
            return False, frame
        except:
            return True, cv2.imread(self.image_paths[0])
