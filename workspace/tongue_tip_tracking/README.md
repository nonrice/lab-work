# `tongue_tip_track.py`

## Usage as module
`import tongue_tip_track`

### `tongue_tip_track.find_tongue_tip(img)`
Uses 2D analogue of tip tracking algorithm in [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8299742/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8299742/) to return tongue tip coordinates in `img`. `img` as boolean matrix.

### `tongue_tip_track.load_bool_img(path)`
Returns image at `path` as boolean matrix.

### `tongue_tip-track.plot_tip(img, tip)`
Opens a matplotlib plot of `tip` plotted upon `img`.

## Usage as CLI
`python tongue_tip_track.py --help`
