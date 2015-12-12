# Test images from US National Cancer Institute

Images downloaded from the [National Cancer Institute's (NCI) Visuals Online service](https://visuals.nci.nih.gov/). The images are in the public domain, credits and details are copied below.

Low resolution versions are included here to keep the repository size down. High resolution versions are available.

## nci-vol-2304-72.jpg

| Title | Normal Cells |
------------------------
| Source | <https://visualsonline.cancer.gov/details.cfm?imageid=2304> |
| Description | Normal cells of human connective tissue in culture. At a magnification of 500x, the cells were illuminated by darkfield amplified contrast technique. This image compares to the cancerous cells on <http://visuals.nci.nih.gov/details.cfm?imageid=2306> |
| Source | National Cancer Institute |
| Creator | Dr. Cecil Fox (Photographer) | 
| AV Number | AV-8711-3168 | 
| Date Created | November 1987 |
| Reuse Restrictions | None - This image is in the public domain and can be freely reused. Please credit the source and/or author listed above. |

## nci-vol-2306-72.jpg

| Title | Cancer Cells |
------------------------
| Source | <https://visuals.nci.nih.gov/details.cfm?imageid=2306> |
| Description | Cancer cells in culture from human connective tissue, illuminated by darkfield amplified contrast, at a magnification of 500x. These cells can be compared to normal cells on <http://visuals.nci.nih.gov/details.cfm?imageid=2304> |
| Source | National Cancer Institute |
| Creator | Dr. Cecil Fox (Photographer) |
| AV Number | AV-8711-3170 |
| Date Created | November 1987 |
| Reuse Restrictions | None - This image is in the public domain and can be freely reused. Please credit the source and/or author listed above |

## nci-vol-2303-72.jpg

| Title | Normal Cells |
------------------------
| Source | <http://visuals.nci.nih.gov/details.cfm?imageid=2303> |
| Description | Normal cells from human connective tissue in culture at a magnification of 500x, using a darkfield amplified contrast technique. This slide can be compared to cancerous cells on <http://visuals.nci.nih.gov/details.cfm?imageid=2305> |
| Source | National Cancer Institute | 
| Creator | Dr. Cecil Fox (Photographer) | 
| AV Number | AV-8711-3167 |
| Date Created | November 1987 |
| Reuse Restrictions | None - This image is in the public domain and can be freely reused. Please credit the source and/or author listed above |

## nci-vol-2305-72.jpg

| Title | Cancer Cells |
------------------------
| Source | <http://visuals.nci.nih.gov/details.cfm?imageid=2305> |
| Description | Cancer cells in tissue culture from human connective tissue, illuminated by darkfield amplified contrast, at a magnification of 500x. These cells can be compared to normal cells in <http://visuals.nci.nih.gov/details.cfm?imageid=2303> | 
| Source | National Cancer Institute |
| Creator | Dr. Cecil Fox (Photographer) |
| AV Number | AV-8711-3169 |
| Date Created | November 1987 |
| Reuse Restrictions | None - This image is in the public domain and can be freely reused. Please credit the source and/or author listed above |

## Tile generation

For test purposes, static files were created with `iiif_static.py` from <https://github.com/zimeon/iiif>:

```
simeon@RottenApple manifest-factory>iiif_static.py --dst=testimages testimages/*.jpg 
testimages / nci-vol-2303-72/0,0,512,432/512,/0/default.jpg
testimages / nci-vol-2303-72/512,0,136,432/136,/0/default.jpg
testimages / nci-vol-2303-72/full/324,/0/default.jpg
testimages / nci-vol-2303-72/full/324,216 -> nci-vol-2303-72/full/324,
testimages / nci-vol-2303-72/full/162,/0/default.jpg
testimages / nci-vol-2303-72/full/162,108 -> nci-vol-2303-72/full/162,
testimages / nci-vol-2303-72/full/81,/0/default.jpg
testimages / nci-vol-2303-72/full/81,54 -> nci-vol-2303-72/full/81,
testimages / nci-vol-2303-72/full/41,/0/default.jpg
testimages / nci-vol-2303-72/full/41,27 -> nci-vol-2303-72/full/41,
testimages / nci-vol-2303-72/full/20,/0/default.jpg
testimages / nci-vol-2303-72/full/20,14 -> nci-vol-2303-72/full/20,
testimages / nci-vol-2303-72/full/10,/0/default.jpg
testimages / nci-vol-2303-72/full/10,7 -> nci-vol-2303-72/full/10,
testimages / nci-vol-2303-72/full/5,/0/default.jpg
testimages / nci-vol-2303-72/full/5,3 -> nci-vol-2303-72/full/5,
testimages / nci-vol-2303-72/full/3,/0/default.jpg
testimages / nci-vol-2303-72/full/3,2 -> nci-vol-2303-72/full/3,
testimages / nci-vol-2303-72/full/1,/0/default.jpg - zero size, skipped
testimages / nci-vol-2303-72/info.json
...
```
