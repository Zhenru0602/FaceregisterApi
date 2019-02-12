# USAGE
# python encode_faces.py --user user --image image

# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import json
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--user", required=True,
	help="user name")
ap.add_argument("-i", "--image", required=True,
	help="image name")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

os.makedirs("face-recognition-opencv/dataset/" + args["user"])
os.rename("face-recognition-opencv/"+args["image"], "face-recognition-opencv/dataset/" + args["user"] + "/" + args["image"])

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images("face-recognition-opencv/dataset/"+args["user"]))

# initialize the list of known encodings and known names
# data = json.load(open("face-recognition-opencv/encodings.json", "rb").read())
# knownEncodings = data["encodings"]
# knownNames = data["names"]
if not os.path.isfile('face-recognition-opencv/encodings.json'):
	with open('face-recognition-opencv/encodings.json', mode='w', encoding='utf-8') as f:
		json.dump([], f)

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]
	print(imagePath)

	# load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	max_width = 800
	if max_width < image.shape[1]:
		scaling = max_width / float(image.shape[1])
		image = cv2.resize(image, None, fx=scaling, fy=scaling, interpolation=cv2.INTER_CUBIC)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)

	# loop over the encodings
	with open('face-recognition-opencv/encodings.json') as f:
		feeds = json.load(f)
	with open('face-recognition-opencv/encodings.json', mode='w', encoding='utf-8') as f:
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			# knownEncodings.append(encoding)
			# knownNames.append(name)
			entry = {'name': 'name', 'encoding': 'encoding'}
			feeds.append(entry)
		json.dump(feeds, f)

# dump the facial encodings + names to disk
# print("[INFO] serializing encodings...")
# data = {"encodings": knownEncodings, "names": knownNames}
# f = open("face-recognition-opencv/encodings.pickle", "wb")
# f.write(pickle.dumps(data))
# f.close()
print("[INFO] write success")
