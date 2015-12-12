"""Test code for iiif_prezi.loader using remote data."""

from iiif_prezi.loader import ManifestReader
import urllib, os, sys

def test_remote():
	"""Test a list or remote Manifest URLs."""
	urls = [
	 #"http://dms-data.stanford.edu/data/manifests/Walters/qm670kv1873/manifest.json",
	 #"http://manifests.ydc2.yale.edu/manifest/Admont23.json",
	 #"http://oculus-dev.lib.harvard.edu/manifests/drs:5981093",
	 #"http://iiif-dev.bodleian.ox.ac.uk/metadata/bib_germ_1485_d1/bib_germ_1485_d1.json",
	 #"http://iiif-dev.bodleian.ox.ac.uk/metadata/ms_auct_t_inf_2_1/ms_auct_t_inf_2_1.json",
	 #"http://demos.biblissima-condorcet.fr/iiif/metadata/ark:/12148/btv1b84473026/manifest.json",
	 #"http://demos.biblissima-condorcet.fr/iiif/metadata/ark:/12148/btv1b84473026/manifest-ranges.json",
	 #"http://demos.biblissima-condorcet.fr/mirador/data/add_ms_10289_edited_8v-9r.json",
	 #"http://demos.biblissima-condorcet.fr/iiif/metadata/ark:/12148/btv1b8438674r/manifest.json",
	 "http://demos.biblissima-condorcet.fr/iiif/metadata/BVH/B410186201_LI03/manifest.json",
	 "http://sanddragon.bl.uk/IIIFMetadataService/add_ms_10289.json",
	 "http://sr-svx-93.unifr.ch/metadata/iiif/bbb-0218/manifest.json",
	 #"http://www.shared-canvas.org/impl/demo1d/res/manifest.json"
	]
	for u in urls:
		fh = urllib.urlopen(u)
		data = fh.read()
		fh.close()
		try:
			print("------")
			print(u)
			reader = ManifestReader(data)
			nmfst = reader.read()
			js = nmfst.toJSON()
		except Exception, e:
			print("   => %s: %s" % (e.__class__.__name__, e))

if __name__ == "__main__":
    test_remote()
