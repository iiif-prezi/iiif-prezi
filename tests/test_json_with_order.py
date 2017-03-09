"""Test code for iiif_prezi.factory."""
import unittest

from iiif_prezi.factory import ManifestFactory


class TestAll(unittest.TestCase):

    def test01_init(self):
        mf = ManifestFactory()
        self.assertEqual(
            mf.context_uri, 'http://iiif.io/api/presentation/2/context.json')
