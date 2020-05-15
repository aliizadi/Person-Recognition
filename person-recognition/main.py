from db import MongoDB
from videos_tracker.tracking import Cameras

if __name__ == '__main__':
    db = MongoDB()
    camera = Cameras(db)

