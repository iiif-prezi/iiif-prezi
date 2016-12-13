"""Test code for iiif_prezi.util."""
import unittest

from iiif_prezi.util import is_http_uri

class TestAll(unittest.TestCase):

    def test01_is_http_uri(self):
        self.assertFalse(is_http_uri(''))
        self.assertFalse(is_http_uri('example.org'))
        self.assertFalse(is_http_uri('/path'))
        self.assertFalse(is_http_uri('ftp://example.org'))
        self.assertTrue(is_http_uri('http://example.org'))
        self.assertTrue(is_http_uri('https://example.org:646/some/path'))
        self.assertTrue(is_http_uri('https://example.org:646/some/path#frag'))
