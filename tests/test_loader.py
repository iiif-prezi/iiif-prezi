"""Test code for iiif_prezi.loader."""
from __future__ import unicode_literals
import re
import unittest
import json

from iiif_prezi.loader import SerializationError, load_document_local, ManifestReader, DataError

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
        self.assertEqual(mf.context_uri, 'http://www.shared-canvas.org/ns/context.json')
        mf = mr.buildFactory('2')
        self.assertEqual(mf.context_uri, 'http://iiif.io/api/presentation/2/context.json')
        # setting in require_version overrides buildFactory() arg
        mr = ManifestReader('dataaa', version='1.0')
        mf = mr.buildFactory('2')
        self.assertEqual(mf.context_uri, 'http://www.shared-canvas.org/ns/context.json')

    def test05_jsonld_to_langhash(self):
        mr = ManifestReader('ab')
        # Errors
        self.assertRaises(DataError, mr.jsonld_to_langhash, [])
        # should this one be caught as a DataError?
        self.assertRaises(TypeError, mr.jsonld_to_langhash, ['@value'])
        self.assertRaises(DataError, mr.jsonld_to_langhash, {})
        self.assertRaises(DataError, mr.jsonld_to_langhash, {'a': 'b'})
        #
        lh = mr.jsonld_to_langhash('a')
        self.assertEqual(lh, 'a')
        lh = mr.jsonld_to_langhash({'@value': 'av'})
        self.assertEqual(lh, 'av')
        lh = mr.jsonld_to_langhash({'@value': 'avz', '@language': 'zz'})
        self.assertEqual(lh, {'zz': 'avz'})

    def test06_labels_and_values(self):
        mr = ManifestReader('ab')
        # Must have label and value
        self.assertRaises(KeyError, mr.labels_and_values, {})
        self.assertRaises(KeyError, mr.labels_and_values, {'label': None})
        self.assertRaises(KeyError, mr.labels_and_values, {'value': None})
        # All possible forms...
        # simple
        lv = mr.labels_and_values({'label': 'l', 'value': 'v'})
        self.assertEqual(lv, {'l': 'v'})
        # dict and list label
        lv = mr.labels_and_values({'label': {'@language': 'en',
                                             '@value': 'lab-en'},
                                   'value': 'v'})
        self.assertEqual(lv, {'label': {'en': 'lab-en'},
                              'value': 'v'})
        lv = mr.labels_and_values({'label': ['label1', 'label2'],
                                   'value': 'v'})
        self.assertEqual(lv, {'label': ['label1', 'label2'],
                              'value': 'v'})
        # dict and list value
        lv = mr.labels_and_values({'label': 'l',
                                   'value': {'@language': 'cz',
                                             '@value': 'val-cz'}})
        self.assertEqual(lv, {'l': {'cz': 'val-cz'}})
        lv = mr.labels_and_values({'label': 'l',
                                   'value': ['val1', 'val2']})
        self.assertEqual(lv, {'l': ['val1', 'val2']})       
