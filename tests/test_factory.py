"""Test code for iiif_prezi.factory"""
from __future__ import unicode_literals
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
        self.assertEqual( mf.default_base_image_uri, 'bb' )
        self.assertEqual( mf.metadata_dir, 'tests/' )
        # language setting
        mf = ManifestFactory(lang='cy')
        self.assertTrue( mf.add_lang )
        self.assertRaises( ConfigurationError, ManifestFactory, version='bad' )

    def test03_set_debug(self):
        mf = ManifestFactory()
        self.assertRaises( ConfigurationError, mf.set_debug, 'unkn' )

    def test10_set_hw_from_file_image_magick(self):
        mf = ManifestFactory()
        self.assertNotEqual( mf.whichid, '' ) #Expect to find ImageMagick
        self.assertRaises( ConfigurationError, mf.image, 'name' )
        mf.set_base_image_uri( 'testimages' )
        img = mf.image('an_image')
        self.assertEqual( img.set_hw_from_file('testimages/nci-vol-2303-72.jpg'), None )
        self.assertEqual( img.width, 648 )
        self.assertEqual( img.height, 432 )

