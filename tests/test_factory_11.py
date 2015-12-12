"""Test code for iiif_prezi.factory_11"""
import unittest

from iiif_prezi.factory_11 import ManifestFactory

class TestAll(unittest.TestCase):

    def test01_init(self):
        mf=ManifestFactory()
        self.assertEqual( mf.context_uri, 'http://www.shared-canvas.org/ns/context.json' )
