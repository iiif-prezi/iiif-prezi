"""Test code for iiif_prezi.factory"""
import unittest

from iiif_prezi.factory import ManifestFactory, ConfigurationError

class TestAll(unittest.TestCase):

    def test01_init(self):
        mf = ManifestFactory()
        self.assertEqual( mf.context_uri, 'http://iiif.io/api/presentation/2/context.json' )
        self.assertFalse( mf.add_lang )
        # simple instance variable sets
        mf = ManifestFactory( mdbase="aa", imgbase="bb", mddir="tests" )
        self.assertEqual( mf.metadata_base, 'aa/' )
        self.assertEqual( mf.default_base_image_uri, '' ) #imgbase gets overridden, odd!
        self.assertEqual( mf.metadata_dir, 'tests/' )
        # language setting
        mf = ManifestFactory(lang='cy')
        self.assertTrue( mf.add_lang )
        self.assertRaises( ConfigurationError, ManifestFactory, version='bad' )

    def test03_set_debug(self):
        mf = ManifestFactory()
        self.assertRaises( ConfigurationError, mf.set_debug, 'unkn' )