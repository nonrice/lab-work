# `tongue_mask_processing`

## Usage as Module
`import tongue_mask_processing`

### `tongue_mask_processing.TongueArchive`
#### `tongue_mask_processing.TongueArchive(filepath)`
Open an HDF5 tongue archive. Respective dataframes in member variables `frames`, `heights`, `widths`, `probs`.

### `tongue_mask_processing.plot_frame(archive, frame_no, img_height, img_width)`
Creates a blank image of dimensions `(img_width, img_height)`. Plots the tongue mask from `archive` at frame `frame_no`. Returns the image as 1-channel matrix.

### `tongue_mask_processing.keep_largest_cc(img)`
Use OpenCV to erase all but the largest connected component in `img` and returns the new image.
