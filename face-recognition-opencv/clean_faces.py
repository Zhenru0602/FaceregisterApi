# import the necessary packages
import pickle
import argparse
import shutil
import os
import timeit

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--user", required=False,
	help="optional selective username")
args = vars(ap.parse_args())
username = args["user"]

start = timeit.default_timer()

if not username:
    print("[INFO] cleaning encodings...")
    data = {"encodings": [], "names": []}
    f = open("encodings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()

    shutil.rmtree('dataset/')
    os.mkdir('dataset/')

else:
    if not os.path.isdir("dataset/"+username):
        print("[ERROR] user not found")
        exit(0)
    
    print("[INFO] cleaning encoding... user", username)
    data = pickle.loads(open("encodings.pickle", "rb").read())
    encodings = data["encodings"]
    names = data["names"]
    assert len(encodings) == len(names)
    for i in range(len(names)-1, -1, -1):
        if names[i] == username:
            names.pop(i)
            encodings.pop(i)
    data = {"encodings":encodings, "names":names}
    f = open("encodings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()

    shutil.rmtree("dataset/"+username)

end = timeit.default_timer()

print("[INFO] cleaning done! Hooray!")
print("[INFO] duration:", end-start)
