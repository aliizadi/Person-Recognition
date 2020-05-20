from collections import OrderedDict

import cv2
import numpy as np
from scipy.spatial import distance as dist

from videos_tracker.algorithms import recognize_faces


class CentroidTracker:
	def __init__(self, db, camera_id, max_frames_disappeared=50, max_distance=50):
		
		self.id = camera_id
		self.db = db
		self.next_face_id = 0
		self.faces = OrderedDict()
		self.disappeared = OrderedDict()
		self.appeared = OrderedDict()

		self.max_frames_disappeared = max_frames_disappeared
		self.max_distance = max_distance

	def register(self, centroid, trackable_face):
		self.faces[self.next_face_id] = [centroid, TrackableFace(trackable_face[0], trackable_face[1], trackable_face[2], trackable_face[3], trackable_face[4])]
		self.disappeared[self.next_face_id] = 0
		self.appeared[self.next_face_id] = 0
		self.next_face_id += 1

	def deregister(self, face_id):
		if self.appeared[face_id] > 20:
			self.__recognize_face(face_id)

		del self.faces[face_id]
		del self.disappeared[face_id]
		del self.appeared[face_id]

	def __draw_rectangle(self, face):

		for i in range(len(face.images)):
			(left, top, right, bottom) = face.rects[i]
			cv2.rectangle(face.images[i], (left, top), (right, bottom), (0, 255, 0), 2)

	def __recognize_face(self, face_id):
		face = self.faces[face_id][1]
		self.__draw_rectangle(face)

		known_persons_encodings, known_persons_indices, known_persons_ids = self.__create_person_encodings()

		largeset_face_args = self.__get_largest_faces_args(face)

		unknown_person_encodings = [face.encodings[i] for i in largeset_face_args]
		unknown_person_faces = [face.images[i] for i in largeset_face_args]
		dates = [face.dates[i] for i in largeset_face_args]
		times = [face.times[i] for i in largeset_face_args]

		found_person = recognize_faces(known_persons_encodings, known_persons_indices, unknown_person_encodings[-1])

		self.__add_track(found_person, unknown_person_encodings, unknown_person_faces, known_persons_encodings, known_persons_indices, known_persons_ids, dates, times)

		self.face_encodings = []
		self.frames = []

	def __get_largest_faces_args(self, face, k=10):
		faces_size = [abs(bottom-top) * abs(right-left) for (left, top, right, bottom) in face.rects]
		sorted_face_args = np.argsort(faces_size)
		largeset_face_args = [sorted_face_args[i] for i in range(int(len(sorted_face_args)/2), int(len(sorted_face_args)/2 + k)) ]
		return largeset_face_args

	def __create_person_encodings(self):
		persons_encodings = self.db.get_encodings()
		known_persons_encodings = []
		known_persons_indices = []
		known_persons_ids = []
		for i, person_encoding in enumerate(persons_encodings):
			id = person_encoding['id']
			known_persons_indices.extend([i for _ in range(len(person_encoding['encoding']))])
			known_persons_ids.extend([id  for _ in range(len(person_encoding['encoding']))])
			known_persons_encodings.extend(person_encoding['encoding'])
		
		return known_persons_encodings, known_persons_indices, known_persons_ids

	def __add_track(self, found_person, unknown_person_encodings, unknown_person_faces, known_persons_encodings, known_persons_indices, known_persons_ids, dates, times):

		def new_person(person):
			return person == -1

		if new_person(found_person):
			print('new person')
			encoding_id = self.db.add_encoding(np.array(unknown_person_encodings).tolist(), self.id)
			track_id = self.db.add_track(encoding_id, self.id, dates[-1], times[-1])
			image_id = self.db.add_image(encoding_id, track_id)
			self.__save_image(unknown_person_faces[-1], image_id)
		
		else:
			print('old person')
			encodings = []
			encoding_id = None
			for i, index in enumerate(known_persons_indices):
				if index == found_person:
					encodings.append(known_persons_encodings[i])
					encoding_id = known_persons_ids[i]

			encodings.extend(np.array(unknown_person_encodings).tolist())


			self.db.update_encoding(encoding_id, encodings)
			track_id = self.db.add_track(encoding_id, self.id, dates[-1], times[-1])
			image_id = self.db.add_image(encoding_id, track_id)
			self.__save_image(unknown_person_faces[-1], image_id)

    
	def __save_image(self, frame, image_id):
		# print('trying to save image')
		cv2.imwrite(f'static/images/{image_id}.png', frame)
		print('image saved')


	def update(self, frames_information):
		# print('----------------------------', len(self.faces))
		
		rects = [frame_information[0] for frame_information in frames_information] 
		trackable_face = [(frame_information[1], frame_information[2], frame_information[3], frame_information[4], frame_information[0]) for frame_information in frames_information] 
		# print(rects)
		if len(rects) == 0:
			# print('all faces disappeared')
			self.__all_faces_disappeared()
			return self.faces

		input_centroids = self.__compute_rects_centers(rects)

		if len(self.faces) == 0:
			# print('first new faces appeared')
			self.__first_new_faces_appeared(input_centroids, trackable_face)
		else:
			# print('track by centroids')
			self.__track_by_centroids(input_centroids, trackable_face)

		return self.faces

	def __track_by_centroids(self, input_centroids, trackable_face):
		face_ids = list(self.faces.keys())
		face_centroids = [face[0] for face in list(self.faces.values())]

		pairwise_distances = dist.cdist(np.array(face_centroids), input_centroids)

		nearest_centers_rows = pairwise_distances.min(axis=1).argsort()
		cols = pairwise_distances.argmin(axis=1)[nearest_centers_rows]

		used_rows = set()
		used_cols = set()

		for (row, col) in zip(nearest_centers_rows, cols):
			if row in used_rows or col in used_cols:
				continue

			if pairwise_distances[row, col] > self.max_distance:
				continue

			face_id = face_ids[row]
			self.faces[face_id][0] = input_centroids[col]
			
			to_be_updated_trackable_face = self.faces[face_id][1]
			if trackable_face[col][0] is not None:

				to_be_updated_trackable_face.add_encoding(trackable_face[col][0])
				to_be_updated_trackable_face.add_image(trackable_face[col][1])
				to_be_updated_trackable_face.add_date(trackable_face[col][2])
				to_be_updated_trackable_face.add_time(trackable_face[col][3])
				to_be_updated_trackable_face.add_rect(trackable_face[col][4])

			self.disappeared[face_id] = 0
			self.appeared[face_id] += 1

			used_rows.add(row)
			used_cols.add(col)

		unused_rows = set(range(0, pairwise_distances.shape[0])).difference(used_rows)
		unused_cols = set(range(0, pairwise_distances.shape[1])).difference(used_cols)

		if pairwise_distances.shape[0] >= pairwise_distances.shape[1]:
			self.__some_faces_disappeared(unused_rows, face_ids)

		else:
			self.__new_faces_appeared(unused_cols, input_centroids, trackable_face)


	def __new_faces_appeared(self, unused_cols, input_centroids, trackable_face):
		for col in unused_cols:
			self.register(input_centroids[col], trackable_face[col])

	def __some_faces_disappeared(self, unused_rows, face_ids):
		for row in unused_rows:
			face_id = face_ids[row]
			self.disappeared[face_id] += 1
			if self.disappeared[face_id] > self.max_frames_disappeared:
				self.deregister(face_id)

	def __first_new_faces_appeared(self, input_centroids, trackable_face):
		self.__new_faces_appeared(range(0, len(input_centroids)), input_centroids, trackable_face)

	def __all_faces_disappeared(self):
		for face_id in list(self.disappeared.keys()):
			self.disappeared[face_id] += 1
			if self.disappeared[face_id] > self.max_frames_disappeared:
				self.deregister(face_id)

	def __compute_rects_centers(self, rects):
		input_centroids = np.zeros((len(rects), 2), dtype="int")

		for (i, (startX, startY, endX, endY)) in enumerate(rects):
			cX = int((startX + endX) / 2.0)
			cY = int((startY + endY) / 2.0)
			input_centroids[i] = (cX, cY)
		return input_centroids

class TrackableFace:
	def __init__(self , encoding, image, date, time, rect):
		self.encodings = [encoding]
		self.images = [image]
		self.dates = [date] 
		self.times = [time]
		self.rects = [rect]

	def add_encoding(self, encoding):
		self.encodings.append(encoding)
	
	def add_image(self, image):
		self.images.append(image)
	
	def add_date(self, date):
		self.dates.append(date)
	
	def add_time(self, time):
		self.times.append(time)
	
	def add_rect(self, rect):
		self.rects.append(rect)
