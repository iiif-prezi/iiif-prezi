"""iiif-prezi example code to build a manifest from a directory of images

"""

from iiif_prezi.factory import ManifestFactory
import os

image_dir = "/path/to/images"
prezi_dir = "/tmp"

fac = ManifestFactory()
fac.set_debug("error")
fac.set_base_image_uri("http://localhost/iiif")
fac.set_base_image_dir(image_dir)
fac.set_iiif_image_info()
fac.set_base_prezi_uri("http://localhost/prezi/")
fac.set_base_prezi_dir(prezi_dir)

mflbl = os.path.split(image_dir)[1].replace("_", " ").title()

mfst = fac.manifest(label=mflbl)
seq = mfst.sequence()
for fn in os.listdir(image_dir):
    ident = fn[:-4]
    title = ident.replace("_", " ").title()
    cvs = seq.canvas(ident=ident, label=title)
    cvs.add_image_annotation(ident, True)

mfst.toFile(compact=False)
