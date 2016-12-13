"""Test code for iiif_prezi.loader."""
from __future__ import unicode_literals
import re
import unittest

from iiif_prezi.loader import SerializationError, load_document_local, ManifestReader

class TestAll(unittest.TestCase):

    def test01_init_serialization_error(self):
        e = SerializationError('oops')
        self.assertEqual( str(e), 'oops' )

    def test02_load_document_local(self):
        doc1 = load_document_local('http://iiif.io/api/presentation/2/context.json')
        self.assertEqual( doc1['documentUrl'], None )
        self.assertEqual( doc1['contextUrl'], None )
        self.assertTrue( re.search( r'''http://iiif.io/api/presentation/2#''', doc1['document'] ) )
        doc2 = load_document_local('whatever')
        self.assertEqual( doc2['documentUrl'], None )
        self.assertEqual( doc2['contextUrl'], None )
        self.assertTrue( re.search( r'''http://library.stanford.edu/iiif/image-api/ns/''', doc2['document'] ) )

    def test03_init(self):
        mr = ManifestReader('oopsee')
        self.assertEqual( mr.data, 'oopsee' )
        self.assertEqual( mr.require_version, None )
        # init doesn't do much else

    def test04_buildFactory(self):
        mr = ManifestReader('dataaa')
        mf = mr.buildFactory('1.0')
        self.assertEqual( mf.context_uri, 'http://www.shared-canvas.org/ns/context.json' )
        mf = mr.buildFactory('2')
        self.assertEqual( mf.context_uri, 'http://iiif.io/api/presentation/2/context.json' )
        # setting in require_version overrides buildFactory() arg
        mr = ManifestReader('dataaa', version='1.0')
        mf = mr.buildFactory('2')
        self.assertEqual( mf.context_uri, 'http://www.shared-canvas.org/ns/context.json' )

