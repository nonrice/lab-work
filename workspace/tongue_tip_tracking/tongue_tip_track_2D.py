import numpy as np 
from matplotlib import pyplot as plt
from numba import njit, jit, prange 
from numba.types import bool_

@njit("float32[:](int32[:, :])", parallel=True)
def centroid(a):
    """
    Calculate the centroid of an array of 2D points.

    Parameters:
    a (numpy.ndarray): The input array of shape (n, 2).

    Returns:
    numpy.ndarray: The centroid coordinates as a 1D array of shape (2,).

    """
    return np.array([np.mean(a[:, 0]), np.mean(a[:, 1])], dtype=np.float32)

@njit("float32(float32, float32, float32)")
def clip(a, min_val, max_val):
    """
    Clip a value to a specified range.

    Parameters:
    a (np.float32): The input value.
    min_val (np.float32): The minimum value.
    max_val (np.float32): The maximum value.

    Returns:
    np.float32: The clipped value.
    """
    return np.minimum(np.maximum(a, min_val), max_val)

@njit("bool_[:](bool_[:, :], int32[:, :])", parallel=True)
def v_is_boundary(img, a):
    """
    For each point in a, check if it is a boundary point in img using 8-connectivity.

    Parameters:
    img (numpy.ndarray): The input binary image.
    a (numpy.ndarray): The input array of 2D points of shape (n, 2).

    Returns:
    numpy.ndarray: The boolean array of shape (n,) correspondig to a, indicating if the point is a boundary point.
    """
    ans = np.zeros(a.shape[0], dtype=bool_)
    for i in prange(a.shape[0]):
        if img[a[i][1]][a[i][0]] == 0:
            continue 
        for dy in prange(-1, 2):
            for dx in prange(-1, 2):
                ans[i] |= (a[i][0]+dx<img.shape[1] and a[i][1]+dy<img.shape[0] and a[i][0]+dx>=0 and a[i][1]+dy>=0 and img[a[i][1] + dy][a[i][0] + dx] == 0)
    return ans

@njit("float32[:](float32[:, :])", parallel=True)
def v_norm(a):
    """
    Compute magnitude of each 2D vector in a

    Parameters:
    a (numpy.ndarray): The input array of 2D vectors of shape (n, 2).

    Returns:
    numpy.ndarray: The magnitude of each vector in a as a 1D array of shape (n,).
    """
    ans = np.zeros(a.shape[0], dtype=np.float32)
    for i in prange(a.shape[0]):
        ans[i] = np.sqrt(a[i][0]*a[i][0] + a[i][1]*a[i][1])
    return ans

@njit("float32[:](float32[:, :], float32[:])", parallel=True)
def v_angle(a, v2):
    """
    Compute the angle between each 2D vector in a and a fixed vector v2.

    Parameters:
    a (numpy.ndarray): The input array of 2D vectors of shape (n, 2).
    v2 (numpy.ndarray): The fixed 2D vector of shape (2,).

    Returns:
    numpy.ndarray: The angle between each vector in a and v2 as a 1D array of shape (n,).
    """
    ans = np.zeros(a.shape[0], dtype=np.float32)
    n1 = v_norm(a)
    v2 = v2.astype(np.float32)
    n2 = np.linalg.norm(v2.astype(np.float32))
    d = np.dot(np.ascontiguousarray(a), v2)
    if n2 == 0:
        return ans
    for i in prange(a.shape[0]):
        if n1[i] == 0:
            ans[i] = 0
            continue
        ans[i] = np.degrees(np.math.acos(clip(d[i] / (n1[i] * n2), np.float32(-1), np.float32(1))))
    return ans

@njit("float32[:](bool_[:, :], float32[:])", parallel=True)
def find_tongue_tip(img, init_vec):
    """
    Find the tongue tip from a binary mask of the tongue.
    
    Parameters:
    img (numpy.ndarray): The input binary image.
    
    Returns:
    numpy.ndarray: The tongue tip coordinates as a 1D array of shape (2,).
    """
    mask = np.column_stack(np.where(img == 1)[::-1]).astype(np.int32)
    c1 = centroid(mask)

    dists = v_norm(c1 - mask)
    dist75 = int(sorted(dists)[int(0.75 * len(dists))])

    v1 = init_vec 
    cand1 = mask[np.where(np.logical_and(v_norm(mask - c1) > dist75, v_angle(mask - c1, v1) < 45))]

    if len(cand1) == 0:
        return c1
    c2 = centroid(cand1) 
    v2 = c2 - c1
    cand2 = cand1[np.where(np.logical_and(v_angle(cand1-c1, v2) < 15, v_is_boundary(img, cand1)))]

    if len(cand2) == 0:
        return c2
    return centroid(cand2)

@njit("float32[:](bool_[:, :], float32[:])", parallel=True)
def find_tongue_tip_no_dist(img, init_vec):
    """
    Find the tongue tip from a binary mask of the tongue, without using the 75th percentile
    distance to filter out the tongue body. Useful for bottom view of tongue where tongue may be
    wider than it is long.

    Parameters:
    img (numpy.ndarray): The input binary image.

    Returns:
    numpy.ndarray: The tongue tip coordinates as a 1D array of shape (2,).
    """
    mask = np.column_stack(np.where(img == 1)[::-1]).astype(np.int32)
    c1 = centroid(mask)

    v1 = init_vec 
    cand1 = mask[np.where(v_angle(mask - c1, v1) < 45)]

    if len(cand1) == 0:
        return c1
    c2 = centroid(cand1) 
    v2 = c2 - c1
    cand2 = cand1[np.where(np.logical_and(v_angle(cand1-c1, v2) < 15, v_is_boundary(img, cand1)))]

    if len(cand2) == 0:
        return c2
    return centroid(cand2)

def load_bool_img(path):
    """
    Utility function to load a binary image from a file.

    Parameters:
    path (str): The path to the image file.

    Returns:
    numpy.ndarray: The binary image as a 2D numpy array.
    """
    img = plt.imread(path)
    grayscale_img = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])
    threshold = 0.5
    binarized_img = grayscale_img > threshold
    return np.array(binarized_img, dtype=np.bool_)

def plot_tip(img, tip):
    """
    Utility function to plot the image with the tongue tip.
    
    Parameters:
    img (numpy.ndarray): The input binary image.
    tip (numpy.ndarray): The tongue tip coordinates as a 1D array of shape (2,).

    Returns:
    None
    """
    plt.imshow(img, cmap="gray")
    plt.scatter(x = tip[0], y = tip[1], c = "r", s = 10);
    plt.show()

if __name__ == "__main__":
    # Command line usage
    import argparse
    parser = argparse.ArgumentParser(description="Find tongue tip from binary mask.")
    parser.add_argument("--in_path", required=True, help="Input image of binary mask")
    parser.add_argument("--show", action="store_true", help="Show the image with the tongue tip")
    args = parser.parse_args()
    img = load_bool_img(args.in_path)
    tip = find_tongue_tip(img, np.array([-1, 0], dtype=np.float32))
    if args.show:
        plot_tip(img, tip)
    else:
        print(tip)