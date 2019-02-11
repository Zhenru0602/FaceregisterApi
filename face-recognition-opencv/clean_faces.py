# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

data = pickle.loads(open("encodings.pickle", "rb").read())
print("cleaning encodings...")
data = {"encodings": [], "names": []}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()