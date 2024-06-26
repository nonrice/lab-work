from matplotlib import pyplot as plt
import numpy as np

def centroid()

img_path = "./data/maskoutput.png"
img = plt.imread(img_path).astype(bool)

# get centroid c1 as COM of the whole mask
r0 = np.where(img > 0)


pix_cnt = 0
c1 = np.array([0, 0])
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        if img[y][x]:
            pix_cnt += 1
            c1 += [x, y] 
c1 //= pix_cnt

dists = []
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        if img[y][x]:
            dists.append(np.linalg.norm(c1 - np.asarray([x, y])))

# 75th percentile distance from c1
dist75 = sorted(dists)[int(0.75 * len(dists))]

def angle_between(v1, v2):
    return np.degrees(np.math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))

# v1 as intial vector in direction of tongue
v1 = np.array([-1, 1])

# candidate set 1 as pixels farther than dist75 and within 45 deg of v1 
cand1 = []
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        v = np.asarray([x, y]) - c1
        if (
            img[y][x] and
            np.linalg.norm(c1 - np.asarray([x, y])) > dist75 and
            angle_between(v, v1) < 45
        ):
            cand1.append(np.array([x, y]))

# c2 as centroid (COM) of cand1
c2 = sum(cand1) // len(cand1)

def is_boundary(img, x, y):
    if img[y][x] == 0:
        return False
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if x+dx<img.shape[1] and y+dy<img.shape[0] and x+dx>=0 and y+dy>=0 and img[y + dy][x + dx] == 0:
                return True
    return False

# v2 as new search vector
v2 = c2 - c1

# candidate set 2 as pixels within 15 deg of v2 and on boundary
cand2 = []
for x, y in cand1:
    v = np.array([x, y]) - c1
    if angle_between(v, v2) < 15 and is_boundary(img, x, y):
        cand2.append(np.array([x, y]))

# tongue tip is centroid (COM) of cand2
tip = sum(cand2) // len(cand2)
plt.imshow(img, cmap="gray")
plt.scatter(x = tip[0], y = tip[1], c = "r", s = 10);
plt.show()