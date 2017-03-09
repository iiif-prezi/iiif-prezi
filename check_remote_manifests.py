"""Test code for iiif_prezi.loader using remote data."""

import os
import sys
import optparse
try:
    # python3
    from urllib.request import urlopen
except ImportError:
    # fall back to python2
    from urllib2 import urlopen
from iiif_prezi.loader import ManifestReader


TESTSET = [
    # "http://dms-data.stanford.edu/data/manifests/Walters/qm670kv1873/manifest.json",
    # "http://manifests.ydc2.yale.edu/manifest/Admont23.json",
    # "http://oculus-dev.lib.harvard.edu/manifests/drs:5981093",
    # "http://iiif-dev.bodleian.ox.ac.uk/metadata/bib_germ_1485_d1/bib_germ_1485_d1.json",
    # "http://iiif-dev.bodleian.ox.ac.uk/metadata/ms_auct_t_inf_2_1/ms_auct_t_inf_2_1.json",
    # "http://demos.biblissima-condorcet.fr/iiif/metadata/ark:/12148/btv1b84473026/manifest.json",
    # "http://demos.biblissima-condorcet.fr/iiif/metadata/ark:/12148/btv1b84473026/manifest-ranges.json",
    # "http://demos.biblissima-condorcet.fr/mirador/data/add_ms_10289_edited_8v-9r.json",
    # "http://demos.biblissima-condorcet.fr/iiif/metadata/ark:/12148/btv1b8438674r/manifest.json",
    "http://demos.biblissima-condorcet.fr/iiif/metadata/BVH/B410186201_LI03/manifest.json",
    "http://sanddragon.bl.uk/IIIFMetadataService/add_ms_10289.json",
    "http://sr-svx-93.unifr.ch/metadata/iiif/bbb-0218/manifest.json",
    # "http://www.shared-canvas.org/impl/demo1d/res/manifest.json"
]


def read_args():
    """Read command line arguments."""
    p = optparse.OptionParser(description='Check remote manifests by reading with iiif-prezi',
                              usage='usage: %prog [options] [[url]]  (-h for help)')
    p.add_option('--testset', '-t', action='store_true',
                 help='Run against embedded testset')
    (opt, args) = p.parse_args()
    urls = list(args)
    if (opt.testset):
        urls.append(TESTSET)
    if (len(urls) == 0):
        raise Exception("Nothing to check (-h for help)")
    return(urls)


def test_remote(urls):
    """Test a list or remote Manifest URLs."""
    for u in urls:
        fh = urlopen(u)
        data = fh.read()
        fh.close()
        try:
            print("------")
            print(u)
            reader = ManifestReader(data)
            nmfst = reader.read()
            js = nmfst.toJSON()
        except Exception as e:
            print("   => %s: %s" % (e.__class__.__name__, e))

if __name__ == "__main__":
    test_remote(read_args())
