import numpy as np 
from matplotlib import pyplot as plt

def angle_between(v1, v2):
    return np.degrees(np.math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))

def is_boundary(img, p):
    if img[p[1]][p[0]] == 0:
        return False
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if p[0]+dx<img.shape[1] and p[1]+dy<img.shape[0] and p[0]+dx>=0 and p[1]+dy>=0 and img[p[1] + dy][p[0] + dx] == 0:
                return True
    return False

# load image
img_path = "./data/maskoutput.png"
img = plt.imread(img_path).astype(bool)

# get c1 as COM of the whole mask
mask = np.column_stack(np.where(img > 0)[::-1])
c1 = np.mean(mask, axis=0)

# finding 75th percentile distance from c1
dists = np.linalg.norm(c1 - mask, axis=1)
dist75 = int(sorted(dists)[int(0.75 * len(dists))])

# candidate set 1 as pixels farther than dist75 and within 45 deg of v1, v1 as chosen constant
v1 = np.array([-1, 1])
cand1 = list(filter(lambda p : np.linalg.norm(v1 - (p-c1)) > dist75 and angle_between(p-c1, v1) < 45, mask))

# candidate set 2 as pixels within 15 deg of v2 and on mask boundary, where v2 is c2-c1 with c2 as COM of cand1
c2 = np.mean(cand1, axis=0) 
v2 = c2 - c1
cand2 = list(filter(lambda p : angle_between(p-c1, v2) < 15 and is_boundary(img, p), cand1))

# tongue tip is COM of cand2
tip = np.mean(cand2, axis=0) 

plt.imshow(img, cmap="gray")
plt.scatter(x = tip[0], y = tip[1], c = "r", s = 10);
plt.show()