import cv2
import face_recognition
import numpy as np 
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics.pairwise import euclidean_distances


def encode_face(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model='cnn')
    encodings = face_recognition.face_encodings(rgb, boxes)
    return [(box, enc) for (box, enc) in zip(boxes, encodings)]


def find_unique_faces(encodings):
    clt = DBSCAN(metric="euclidean", n_jobs=-1)
    clt.fit(encodings)
    label_ids = np.unique(clt.labels_)
    number_of_unique_faces = len(np.where(label_ids > -1)[0])

    def find_centers(encodings):
        labels = np.array(clt.labels_)
        encodings_np = np.array(encodings)
        clusters = [encodings_np[np.where(labels == label_id)[0]] for label_id in label_ids]
        centers_indices_of_each_cluster = [np.argmin(np.squeeze(euclidean_distances(cluster, [np.average(cluster, axis=0)]))) for cluster in clusters] 

        centers_indices = []
        for m, label_id in enumerate(label_ids):
            if label_id != -1:
                idxs = np.where(clt.labels_ == label_id)[0]
                i = idxs[centers_indices_of_each_cluster[m]]
                centers_indices.append(i)
            
        return centers_indices
        
    centers_indices = find_centers(encodings)

    return centers_indices, number_of_unique_faces


def recognize_faces(known_persons_encodings, unknown_persons_encodings):
    if known_persons_encodings:
        found_persons = []
        for unknown_person_encoding in unknown_persons_encodings:
            matches = face_recognition.compare_faces(known_persons_encodings, unknown_person_encoding, tolerance=0.5)
            if True in matches:
                first_match_index = matches.index(True)
                found_persons.append(first_match_index)
            
            else:
                found_persons.append(-1)
        
        return found_persons
    else:
        return [-1 for i in range(len(unknown_persons_encodings))]
