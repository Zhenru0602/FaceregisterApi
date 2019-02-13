# import the necessary packages
import pickle
import shutil
import os
import timeit

start = timeit.default_timer()
data = pickle.loads(open("encodings.pickle", "rb").read())
print("[INFO] cleaning encodings...")
data = {"encodings": [], "names": []}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()


shutil.rmtree('dataset/')
os.mkdir('dataset/')
end = timeit.default_timer()

print("[INFO] cleaning done! Hooray!")
print("[INFO] duration:", end-start)
