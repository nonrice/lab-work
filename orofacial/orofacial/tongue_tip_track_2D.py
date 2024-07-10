import numpy as np 
from matplotlib import pyplot as plt
from numba import njit, jit, prange 

# https://stackoverflow.com/questions/57500001/numba-failure-with-np-mean
@njit
def centroid(a):
    return np.array([np.mean(a[:, 0]), np.mean(a[:, 1])])

@njit
def clip(a, min_val, max_val):
    return np.minimum(np.maximum(a, min_val), max_val)

@njit
def v_is_boundary(img, a):
    ans = np.zeros(a.shape[0], dtype=np.uint8)
    for i in prange(a.shape[0]):
        if img[a[i][1]][a[i][0]] == 0:
            continue 
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if a[i][0]+dx<img.shape[1] and a[i][1]+dy<img.shape[0] and a[i][0]+dx>=0 and a[i][1]+dy>=0 and img[a[i][1] + dy][a[i][0] + dx] == 0:
                    ans[i] = 1 
    return ans

@njit
def v_norm(a):
    ans = np.zeros(a.shape[0], dtype=np.float64)
    for i in prange(a.shape[0]):
        ans[i] = np.sqrt(a[i][0]*a[i][0] + a[i][1]*a[i][1])
    return ans

@njit
def v_angle(a, v2):
    ans = np.zeros(a.shape[0], dtype=np.float64)
    n1 = v_norm(a)
    v2 = v2.astype(np.float64)
    n2 = np.linalg.norm(v2)
    if n2 == 0:
        return ans
    for i in prange(a.shape[0]):
        if n1[i] == 0:
            ans[i] = 0
            continue
        ans[i] = np.degrees(np.math.acos(clip(np.dot(a[i], v2) / (n1[i] * n2), np.float64(-1), np.float64(1))))
    return ans

@njit
def find_tongue_tip(img, init_vec=np.array([-1, 1])):
    # get c1 as COM of the whole mask
    mask = np.column_stack(np.where(img > 0)[::-1])
    c1 = centroid(mask)

    # finding 75th percentile distance from c1
    dists = v_norm(c1 - mask)
    dist75 = int(sorted(dists)[int(0.75 * len(dists))])

    # candidate set 1 as pixels farther than dist75 and within 45 deg of v1, v1 as chosen constant
    v1 = init_vec 
    cand1 = mask[np.where(np.logical_and(v_norm(mask - c1) > dist75, v_angle(mask - c1, v1) < 45))]

    if len(cand1) == 0:
        return c1
    c2 = centroid(cand1) 
    v2 = c2 - c1
    cand2 = cand1[np.where(np.logical_and(v_angle(cand1-c1, v2) < 15, v_is_boundary(img, cand1)))]

    if len(cand2) == 0:
        return c2
    # tongue tip is COM of cand2
    return centroid(cand2) 

def load_bool_img(path):
    img = plt.imread(path)

    # copilot says this lol
    grayscale_img = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])
    
    threshold = 0.5
    binarized_img = grayscale_img > threshold
    return binarized_img.astype(bool)

def plot_tip(img, tip):
    plt.imshow(img, cmap="gray")
    plt.scatter(x = tip[0], y = tip[1], c = "r", s = 10);
    plt.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Find tongue tip from binary mask.")
    parser.add_argument("--in_path", required=True, help="Input image of binary mask")
    parser.add_argument("--show", action="store_true", help="Show the image with the tongue tip")
    args = parser.parse_args()
    img = load_bool_img(args.in_path)
    tip = find_tongue_tip(img)
    if args.show:
        plot_tip(img, tip)
    else:
        print(tip)