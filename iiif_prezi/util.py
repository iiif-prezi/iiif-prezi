"""IIIF Presentation API - Utility Functions."""

try:  # python 3
    from urllib.parse import urlparse
except:  # python 2
    from urlparse import urlparse

try:
    STR_TYPES = [str, unicode]  # python 2
except:
    STR_TYPES = [bytes, str]  # python 3


def is_http_uri(uri):
    """True if uri is string that is a full http or https URI."""
    if type(uri) not in STR_TYPES:
        return(False)
    up = urlparse(uri)
    return(up.scheme == 'http' or up.scheme == 'https')
