"""Test code for iiif_prezi.loader using fixtures from spec."""
import unittest

from iiif_prezi.factory import DataError, StructuralError, RequirementError, ConfigurationError, PresentationError
from iiif_prezi.loader import SerializationError, ManifestReader

import urllib, os
import difflib
import json


class TestError(PresentationError):
    pass

def print_warnings(reader):
    warns = reader.get_warnings()
    if warns:
        for m in warns:
            print(m[:-1]) 

def do_test(data, excexp):
    debug_tests = 0
    reader = ManifestReader(data)
    if excexp == None:
        # Should pass
        try:
            what = reader.read()
            js = what.toJSON()
            print_warnings(reader)
            return 1
        except Exception as e:        
            print_warnings(reader)
            if debug_tests:
                print("%s:  %s" % (e.__class__.__name__, e))
            return 0
    else:
        # Should raise exception excexp
        try:
            what = reader.read()
            js = what.toJSON()
            if debug_tests:
                print("Loaded okay, should have failed")
                print(json.dumps(js, sort_keys=True, indent=2))
            print_warnings(reader)
            return "no exception"
        except excexp as e:
            # Got expected exception
            return None
        except Exception as e:
            # Not the exception we expected
            return "bad exception, got %s (%s)" % (e.__class__,str(e))

def error(num):
    # Load error manifest number num
    mfid = "http://iiif.io/api/presentation/2.0/example/errors/%d/manifest.json" % (num)
    fn = mfid.replace('http://iiif.io/api/presentation/', 'tests/testdata/' )
    fh = open(fn)
    data = fh.read()
    fh.close()
    reader = ManifestReader(data)
    what = reader.read()
    js = what.toJSON()
    return js

class TestAll(unittest.TestCase):

    def test01_fixtures(self):
        top = 'tests/testdata/2.0/example/fixtures/collection.json'
        fh = open(top)
        data = fh.read()
        fh.close()

        reader = ManifestReader(data)
        ncoll = reader.read()
        # And walk the manifests
        for manifest in ncoll.manifests:
            mfid = manifest.id
            fn = mfid.replace('http://iiif.io/api/presentation/', 'tests/testdata/')
            fh = open(fn)
            data = fh.read()
            fh.close()
            #print("Manifest: %s" % mfid)
            diff = ''
            js2 = ''
            try:
                js = json.loads(data)
                reader = ManifestReader(data)
                nman = reader.read()
                js2 = nman.toJSON(top=True)
                # Construct helpful diff...
                if js != js2:
                    data2 = nman.toString(compact=False)
                    diff += "diff:\nin: %s  out: %s" % (len(data), len(data2))
                    diff += "- is in, + is out"
                    for x in difflib.unified_diff(data.split('\n'), data2.split('\n')):
                        diff += x
            except Exception as e:
                diff = "Read failed with exception: %s" % (str(e))
            self.assertEqual( js, js2, "Manifest %s: %s" % (mfid,diff) )


    def test02_errors(self):
        # Sequence of expected errors based on error example number
        self.assertRaises( SerializationError, error, 0 )
        self.assertRaises( SerializationError, error, 1 )
        self.assertRaises( SerializationError, error, 2 )
        self.assertRaises( SerializationError, error, 3 )
        self.assertRaises( SerializationError, error, 4 )
        self.assertRaises( RequirementError, error, 5 )
        self.assertRaises( StructuralError, error, 6 )
        self.assertRaises( RequirementError, error, 7 )
        self.assertRaises( RequirementError, error, 8 )
        self.assertRaises( RequirementError, error, 9 )
        self.assertRaises( DataError, error, 10 )
        self.assertRaises( StructuralError, error, 11 )
        self.assertRaises( StructuralError, error, 12 )
        self.assertRaises( StructuralError, error, 13 )
        self.assertRaises( StructuralError, error, 14 )
        self.assertRaises( StructuralError, error, 15 )
        self.assertRaises( StructuralError, error, 16 )
        self.assertRaises( StructuralError, error, 17 )
        self.assertRaises( StructuralError, error, 18 )
        self.assertRaises( PresentationError, error, 19 ) # was StructuralError
        self.assertRaises( PresentationError, error, 20 ) # was StructuralError
        self.assertRaises( PresentationError, error, 21 ) # was StructuralError
        self.assertRaises( RequirementError, error, 22 )
        self.assertRaises( RequirementError, error, 23 ) # was ConfigurationError
        self.assertRaises( RequirementError, error, 24 )
        self.assertRaises( PresentationError, error, 25 ) # was DataError
        self.assertRaises( RequirementError, error, 26 )
        self.assertRaises( PresentationError, error, 27 ) # was DataError
        self.assertRaises( RequirementError, error, 28 )
        self.assertRaises( PresentationError, error, 29 ) # was DataError
        self.assertRaises( PresentationError, error, 30 ) # was StructuralError
        self.assertRaises( PresentationError, error, 31 ) # was StructuralError
        self.assertRaises( PresentationError, error, 32 ) # was StructuralError
        self.assertRaises( RequirementError, error, 33 )
        # self.assertRaises( RequirementError, error, 34 ) # was DataError
        self.assertRaises( PresentationError, error, 35 ) # was StructuralError
        self.assertRaises( PresentationError, error, 36 ) # was StructuralError
        self.assertRaises( PresentationError, error, 37 ) # was StructuralError
        self.assertRaises( PresentationError, error, 38 ) # was StructuralError
        self.assertRaises( RequirementError, error, 39 )
        self.assertRaises( PresentationError, error, 40 ) # was StructuralError
        self.assertRaises( RequirementError, error, 41 )
        self.assertRaises( RequirementError, error, 42 ) # was ConfigurationError
        self.assertRaises( PresentationError, error, 43 ) # was DataError
        self.assertRaises( PresentationError, error, 44 ) # was DataError
        #self.assertRaises( DataError, error, 45 ) #FIXME/zimeon py2-py3 diff
        self.assertRaises( DataError, error, 46 )
        #self.assertRaises( DataError, error, 47 ) #FIXME/zimeon py2-py3 diff
        #self.assertRaises( DataError, error, 48 ) #FIXME/zimeon py2-py3 diff
        #self.assertRaises( DataError, error, 49 ) #FIXME/zimeon py2-py3 diff
        self.assertRaises( PresentationError, error, 50 ) # was DataError
        self.assertRaises( RequirementError, error, 51 )
