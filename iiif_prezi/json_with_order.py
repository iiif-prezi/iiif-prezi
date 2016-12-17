"""Hacks to get JSON with ordered entries.

For use in other iiif_prezi modules as:

  from .json_with_order import json, OrderedDict
"""

try:
    import json
except:
    # Fallback for 2.5
    import simplejson as json

try:
    # Only available in 2.7+
    # This makes the code a bit messy, but eliminates the need
    # for the locally hacked ordered json encoder
    from collections import OrderedDict
except:
    # Backported...
    try:
        from ordereddict import OrderedDict
    except:
        raise Exception("To run with old pythons you must: easy_install ordereddict")


