import h5py
import cv2 as cv
import numpy as np

class TongueArchive():
    def __init__(self, filepath):
        """
        Construct a TongueArchive object from a .h5 file.
        
        Parameters:
        filepath (str): The path to the .h5 file.

        Returns:
        TongueArchive: The constructed TongueArchive object.
        """
        self.f = h5py.File(filepath, "r")
        self.frames = self.f.get("frames")
        self.heights = self.f.get("heights")
        self.widths = self.f.get("widths")
        self.probs = self.f.get("probs")

def plot_frame(archive, frame_no, img_height, img_width):
    """
    Plot a frame from the TongueArchive object as a single channel image
    
    Parameters:
    archive (TongueArchive): The TongueArchive object.
    frame_no (int): The frame number.
    img_height (int): The height of the image.
    img_width (int): The width of the image.
    
    Returns:
    numpy.ndarray: The image as a single channel numpy array.
    """
    img = np.zeros((img_height, img_width, 1), dtype=np.uint8)
    img[archive.heights[frame_no], archive.widths[frame_no]] = [255]
    return img

def plot_frame_bool(archive, frame_no, img_height, img_width):
    """
    Plot a frame from the TongueArchive object as a boolean image

    Parameters:
    archive (TongueArchive): The TongueArchive object.
    frame_no (int): The frame number.
    img_height (int): The height of the image.
    img_width (int): The width of the image.

    Returns:
    numpy.ndarray: The image as a boolean numpy array.
    """
    img = np.zeros((img_height, img_width), dtype=np.bool_)
    img[archive.heights[frame_no], archive.widths[frame_no]] = 1
    return img

def keep_largest_cc(img):
    """
    Keep the largest connected component in a binary image

    Parameters:
    img (numpy.ndarray): The input binary image.

    Returns:
    numpy.ndarray: The image with only the largest connected component.
    """
    nb_components, labels, stats, centroids = cv.connectedComponentsWithStats(img, connectivity=4)
    sizes = sorted([(s, i) for i, s in enumerate(stats[:, -1])], reverse=True)

    img[np.where(np.logical_and(labels != sizes[0][1], labels != sizes[1][1]))] = [0]

    return img

if __name__ == "__main__":
    # Sample usage
    arch = TongueArchive("./data/phox2b38_20240307_1_tongue.h5")
    img = plot_frame(arch, 198, 400, 400)
    cv.imwrite("output/raw.png", img)
    img = keep_largest_cc(img)
    cv.imwrite("output/processed.png", img)
