"""Simple example for iiif_prezi.factory.ManifestFactory()."""
    
from iiif_prezi.factory import ManifestFactory
    
factory = ManifestFactory()
factory.set_base_prezi_uri("http://example.org/iiif/prezi/")
factory.set_base_image_uri("http://example.org/iiif/image/")
factory.set_iiif_image_info(version="2.0", lvl="2")

mf = factory.manifest(label="Manifest")
mf.viewingHint = "paged"



seq = mf.sequence()
for x in range(1):
    cvs = seq.canvas(ident="c%s" % x, label="Canvas %s" % x)
    cvs.set_hw(1000,1000)
    anno = cvs.annotation()
    img = factory.image("f1r.c", iiif=True)
    img2 = factory.image("f1r", iiif=True)
    chc = anno.choice(img, [img2])

# print(mf.toString(compact=False))
    
