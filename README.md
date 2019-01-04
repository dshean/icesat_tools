# icesat_tools
Scripts for processing NASA ICESat and ICESat-2 satellite laser altimetry data

## ICESat GLAS

GLAH14 products available from NSIDC:
- [https://nsidc.org/data/GLAH14/versions/34](https://nsidc.org/data/GLAH14/versions/34)
- [http://nsidc.org/data/docs/daac/glas_altimetry/data-dictionary-glah14.html](http://nsidc.org/data/docs/daac/glas_altimetry/data-dictionary-glah14.html)

### Initial download
`lftp ftp://n5eil01u.ecs.nsidc.org/DP5/GLAS/`

`mirror --parallel=16 GLAH14.034`

### Processing
- `glas_proc.py` - clip to specified extent (e.g., CONUS), filter using internal flags/values, filter against reference DEM

### Filtering
- `filter_glas.py` - extract points to match extent of existing raster, analyze statistics for elevation differences. Preparation for pc_align co-registration with ICESat points as reference.

### Analysis
- `glas_analysis` - sample worflow for Africa

### To do
- Update to geopandas
- Add crossover analysis
- Better interpolation
- Remove hardcoded paths, better documentation
