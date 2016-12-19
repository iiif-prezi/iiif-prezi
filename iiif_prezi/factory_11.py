"""IIIF Presentation API v1.1 Manifest Factory."""

from __future__ import unicode_literals
import os, sys, subprocess
import urllib

from .json_with_order import json, OrderedDict
from .util import is_http_uri, STR_TYPES

try:
	subprocess.check_output #should be OK in python2.7 up
except:
	#python2.6, see <http://python-future.org/standard_library_imports.html>
	from future.standard_library import install_aliases
	install_aliases()

try:
	from PIL import Image as pil_image
except:
	try:
		import Image as pil_image
	except:
		pil_image = None

# TODO: New Python image library
# TODO: ImageMagick module
# TODO: VIPS


class ConfigurationError(Exception):
	"""Configuration error."""

	pass

class MetadataError(Exception):
	"""Base metadata exception."""

	pass


VIEWINGHINTS = ['individuals', 'paged', 'continuous']
VIEWINGDIRS = ['left-to-right', 'right-to-left', 'top-to-bottom', 'bottom-to-top']


class ManifestFactory(object):
	"""Factory class for IIIF Presentation API resources, v1.1."""

	metadata_base = ""
	image_base = ""
	metadata_dir = ""
	add_lang = False

	def __init__(self, mdbase="", imgbase="", mddir="", lang="en"):
		"""Initialize ManifestFactory.

		mdbase: (string) URI to which identities will be appended for metadata
		imgbase: (string) URI to which image identities will be appended for IIIF Image API
		mddir: (string) Directory where metadata files will be written
		lang: (string) Language code to use by default if multiple languages given
		"""
		if mdbase:
			self.set_base_metadata_uri(mdbase)
		if imgbase:
			self.set_base_image_uri(imgbase)
		if mddir:
			self.set_base_metadata_dir(mddir)
		self.default_lang = lang
		if self.default_lang != "en":
			self.add_lang = True
		else:
			self.add_lang = False
		self.context_uri = "http://www.shared-canvas.org/ns/context.json"
		self.iiif_profile_uri = "http://library.stanford.edu/iiif/image-api/"
		self.iiif_version = -1
		self.iiif_level = -1
		self.debug_level = "warn"

		# Try to find ImageMagick's identify
		try:
			self.whichid = subprocess.check_output('which identify', shell=True).strip()
		except:
			# No ImageMagick or not unix
			self.whichid = ""

	def set_debug(self, typ):
		"""Set debug level."""
		if typ in ['error', 'warn']:
			self.debug_level = typ
		else:
			raise ConfigurationError("Only levels are 'error' and 'warn'")

	def assert_base_metadata_uri(self):
		"""Check base metadata URI is set."""
		if not self.metadata_base:
			raise ConfigurationError("Metadata API Base URI is not set")

	def assert_base_image_uri(self):
		"""Check base image URI is set."""
		if not self.image_base:
			raise ConfigurationError("IIIF Image API Base URI is not set")

	def set_base_metadata_dir(self, dir):
		"""Set metadata directory.

		Check existance and adds a trailing slash if
		none is present
		"""
		if not os.path.exists(dir):
			raise ConfigurationError("Metadata API Base Directory does not exist")
		elif dir[-1] != "/":
			dir += "/"
		self.metadata_dir = dir

	def set_base_metadata_uri(self, uri):
		"""Set base metadata URI.

		Adds a trailing slash if none is present
		"""
		if not uri:
			raise ValueError("Must provide a URI to set the base URI to")
		elif uri[-1] != "/":
			uri += "/"
		self.metadata_base = uri

	def set_base_image_uri(self, uri):
		"""Set base image URI.

		Adds a trailing slash if none is present
		"""
		if not uri:
			raise ValueError("Must provide a URI to set the base URI to")
		elif uri[-1] != "/":
			uri += "/"	
		self.image_base = uri

	def set_default_label_language(self, lang):
		"""Set default language label."""
		self.default_lang = lang

	def set_iiif_image_conformance(self, version, lvl):
		"""Set IIIF Image API profile and compliance."""
		if not version in ['1.0', '1.1', 1.0, 1.1]:
			raise ConfigurationError("Only versions 1.1 and 1.0 are known")
		if not lvl in [0,1,2]:
			raise ConfigurationError("Level must be 0, 1 or 2")			
		self.iiif_version = float(version)
		self.iiif_level = lvl
		if self.iiif_version == 1.1:
			self.iiif_profile_uri += ("1.1/compliance.html#level%s" % lvl)
		else:
			self.iiif_profile_uri += ("compliance.html#level%s" % lvl)

	def collection(self, ident="collection", label="", mdhash={}):
		"""Create a Collection."""
		self.assert_base_metadata_uri()
		return Collection(self, ident, label, mdhash)

	def manifest(self, ident="manifest", label="", mdhash={}):
		"""Create a Manifest."""
		self.assert_base_metadata_uri()
		return Manifest(self, ident, label, mdhash)

	def sequence(self,ident="", label="", mdhash={}):
		"""Create a Sequence."""
		if ident:
			self.assert_base_metadata_uri()
		return Sequence(self, ident, label, mdhash)

	def canvas(self,ident="", label="", mdhash={}):
		"""Create a Canvas."""
		if ident:
			self.assert_base_metadata_uri()
		return Canvas(self, ident, label, mdhash)

	def annotation(self, ident="", label="", mdhash={}):
		"""Create an Annotation."""
		if ident:
			self.assert_base_metadata_uri()
		return Annotation(self, ident, label=label)

	def annotationList(self, ident="", label="", mdhash={}):
		"""Create an AnnotationList."""
		if not ident:
			raise MetadataError("AnnotationLists must have a real identity")
		return AnnotationList(self, ident, label, mdhash)

	def image(self, ident, label="", iiif=False):
		"""Create an Image."""
		if not ident:
			raise MetadataError("Images must have a real identity")			
		return Image(self, ident, label, iiif)

	def choice(self, default, rest):
		"""Create a Choice."""
		return Choice(self, default, rest)

	def text(self, txt="", ident="", language="", format=""):
		"""Create either a local Text or an ExternalText."""
		if not ident and not txt:
			raise ConfigurationError("Text must have either a URI or embedded text")
		elif txt:
			return Text(self, txt, language, format)
		else:
			return ExternalText(self, ident, language, format)

	def range(self, ident="", label="", mdhash={}):
		"""Create a Range."""
		return Range(self, ident, label, mdhash)

	def layer(self, ident="", label="", mdhash={}):
		"""Create a Layer."""
		return Layer(self, ident, label, mdhash)


class BaseMetadataObject(object):
	"""Base class for metadata resources."""

	def __init__(self, factory, ident="", label="", mdhash={}, **kw):
		"""Initialize BaseMetadataObject."""
		self._factory = factory
		if ident:
			self.id = factory.metadata_base + self.__class__._uri_segment + ident
			if not self.id.endswith('.json'):
				self.id += '.json'
		else:
			self.id = ""
		self.type = self.__class__._type
		self.label = ""
		if label:
			self.set_label(label)
		self.metadata = []
		if mdhash:
			self.set_metadata(mdhash)
		self.description = ""
		self.attribution = ""
		self.license = ""
		self.service = ""
		self.seeAlso = ""
		self.within = ""

	def langhash_to_jsonld(self, lh):
		"""Switch language hash to JSON-LD form.

		In: {"fr": "something in french", "en": "something in english"}
		Out: [{"@value": "something in french", "@language": "fr"}, ...]
		"""
		l = []
		for (k,v) in lh.items():
			l.append({"@value":v, "@language":k})
		return l

	def set_metadata(self, mdhash):
		"""Set metadata property.

		In:  {label:value}
		Set: {"label":label, "value":value}
		Really add_metadata, as won't overwrite
		"""
		for (k,v) in mdhash.items():
			if type(v) in STR_TYPES and self._factory.add_lang:
				v = self.langhash_to_jsonld({self._factory.default_lang : v})
			elif type(v) == dict:
				# "date":{"en:"Circa 1400",fr":"Environ 1400"}
				v = self.langhash_to_jsonld(v)
			self.metadata.append({"label":k, "value":v})

	def set_label(self, label):
		"""Set label property."""
		if type(label) in STR_TYPES and self._factory.add_lang:
			label = self.langhash_to_jsonld({self._factory.default_lang : label})
		elif type(label) == dict:
			# {"en:"Something",fr":"Quelque Chose"}
			label = self.langhash_to_jsonld(v)
		self.label = label
				
	def toJSON(self, top=False):
		"""Serialize as JSON."""
		d = self.__dict__.copy()
		if 'id' in d and d['id']:
			d['@id'] = d['id']
			del d['id']
		d['@type'] = d['type']
		del d['type']
		for (k, v) in d.items():
			if not v or k[0] == "_":
				del d[k]
		for e in self._required:
			if e not in d:
				raise MetadataError("Resource type '%s' requires '%s' to be set" % (self._type, e))
		if self._factory.debug_level == "warn":
			for e in self._warn:
				if e not in d:
					print("WARNING: Resource type '%s' should have '%s' set" % (self._type, e))
		if top:
			d['@context'] = self._factory.context_uri

		# validate enumerations
		if 'viewingHint' in d and not d['viewingHint'] in VIEWINGHINTS:
			raise MetadataError("ViewingHint must be one of: individuals, paged, continuous")
		if 'viewingDirection' in d and not d['viewingDirection'] in VIEWINGDIRS:
			raise MetadataError("ViewingDirection must be one of: left-to-right, right-to-left, top-to-bottom, bottom-to-top")

		return d

	def toString(self, compact=True):
		"""Return JSON setialization as string."""
		js = self.toJSON(top=True)
		if compact:
			return json.dumps(js, sort_keys=True, separators=(',',':'))
		else:
			return json.dumps(js, sort_keys=True, indent=2)

	def toFile(self, compact=True):
		"""Write to local file.

		Creates directories as necessary
		"""
		mdd = self._factory.metadata_dir
		if not mdd:
			raise ConfigurationError("Metadata Directory on Factory must be set to write to file")

		js = self.toJSON(top=True)
		# Now calculate file path based on URI of top object
		# ... which is self for those of you following at home
		myid = js['@id']
		mdb = self._factory.metadata_base
		if not myid.startswith(mdb):
			raise ConfigurationError("The @id of that object is not the base URI in the Factory")

		fp = myid[len(mdb):]	
		bits = fp.split('/')
		if len(bits) > 1:
			mydir = os.path.join(mdd, '/'.join(bits[:-1]))		
			try:
				os.makedirs(mydir)
			except OSError as e:
				pass

		fh = open(os.path.join(mdd, fp), 'w')
		if compact:
			json.dump(js, fh, sort_keys=True, separators=(',',':'))
		else:
			json.dump(js, fh, sort_keys=True, indent=2)
		fh.close()

class ContentResource(BaseMetadataObject):
	"""Content resource referred to in prezi API."""

	def make_selection(self, selector, summarize=False):
		"""Create SpecificResource for selector."""
		if summarize:
			full = {"@id":self.id, "@type": self.type}
			if self.label:
				full['label'] = self.label
		else:
			full = self

		sr = SpecificResource(self._factory, full)
		if type(selector) == str:
			selector = {"@type": "oa:FragmentSelector", "value": selector}
		sr.selector = selector
		return sr

	def make_fragment(self, fragment):
		"""Return id with URI fragment added."""
		return self.id + "#" + fragment


class Collection(BaseMetadataObject):
	"""Collection object in Presentation API."""

	_type = "sc:Collection"
	_uri_segment = ""
	_required = ["@id", 'label']
	_warn = []
	collections = []
	manifests = []

	def __init__(self, *args, **kw):
		"""Initialize Collection."""
		self.collections = []
		self.manifests = []
		return super(Collection, self).__init__(*args, **kw)

	def add_collection(self, coll):
		"""Add add_collection to this Collection."""
		self.collections.append(coll)

	def add_manifest(self, manifest):
		"""Add Manifest to this Collection."""
		self.manifests.append(manifest)

	def collection(self, *args, **kw):
		"""Create Collection and add to this Collection."""
		coll = self._factory.collection(*args, **kw)
		self.add_collection(coll)
		return coll

	def manifest(self, *args, **kw):
		"""Create Manifest and add to this Collection."""
		mn = self._factory.manifest(*args, **kw)
		self.add_manifest(mn)
		return mn

	def toJSON(self, top=True):
		"""Serialize as JSON."""
		json = super(Collection, self).toJSON(top)
		newcolls = []
		newmans = []
		if 'collections' in json:
			# Add in only @id, @type, label
			for c in json['collections']:
				newcolls.append({"@id": c.id, '@type': 'sc:Collection', 'label': c.label})
			json['collections'] = newcolls
		if 'manifests' in json:
			# Add in only @id, @type, label
			for c in json['manifests']:
				newmans.append({"@id": c.id, '@type': 'sc:Manifest', 'label': c.label})
			json['manifests'] = newmans
		return json


class Manifest(BaseMetadataObject):
	"""Manifest object in Presentation API."""

	_type = "sc:Manifest"
	_uri_segment = ""
	_required = ["@id", "label", "sequences"]
	_warn = ["description"]
	sequences = []
	structures = []

	def __init__(self, *args, **kw):
		"""Initialize Manifest."""
		self.sequences = []
		self.structures = []
		return super(Manifest, self).__init__(*args, **kw)

	def add_sequence(self, seq):
		"""Add Sequence to this Manifest.
		
		Verify identity doesn't conflict with existing sequences
		"""
		if seq.id:
			for s in self.sequences:
				if s.id == seq.id:
					raise MetadataError("Cannot have two Sequences with the same identity")
		self.sequences.append(seq)

	def add_range(self, rng):
		"""Add Range to this Manifest.

		Verify identity doesn't conflict with existing ranges
		"""
		if rng.id:
			for r in self.structures:
				if r.id == rng.id:
					raise MetadataError("Cannot have two Ranges with the same identity")
		self.structures.append(rng)

	def sequence(self, *args, **kw):
		"""Create Sequance and add to this Manifest."""
		seq = self._factory.sequence(*args, **kw)
		self.add_sequence(seq)
		return seq

	def range(self, *args, **kw):
		"""Create Range and add to this Manifest."""
		rng = self._factory.range(*args, **kw)
		self.add_range(rng)
		return rng

	def toJSON(self, top=True):
		"""Serialize as JSON."""
		json = super(Manifest, self).toJSON(top)
		newseqs = []

		for s in json['sequences']:			
			if isinstance(s, Sequence):
				newseqs.append(s.toJSON(False))
			elif type(s) == dict and dict['@type'] == 'sc:Sequence':
				newseqs.append(s)
			else:
				raise MetadataError("Non-Sequence in Manifest['sequences']")
		json['sequences'] = newseqs
		if 'structures' in json:
			newstructs = []
			for s in json['structures']:
				newstructs.append(s.toJSON(False))
			json['structures'] = newstructs
		return json


class Sequence(BaseMetadataObject):
	"""Sequence object in Presentation API."""

	_type = "sc:Sequence"
	_uri_segment = "sequence/"
	_required = ["canvases"]
	_warn = ["@id", "label"]
	canvases = []

	def __init__(self, *args, **kw):
		"""Initialize Sequence."""
		self.canvases = []
		return super(Sequence, self).__init__(*args, **kw)

	def add_canvas(self, cvs):
		"""Add Canvas to this Sequence."""
		if cvs.id:
			for c in self.canvases:
				if c.id == cvs.id:
					raise MetadataError("Cannot have two Canvases with the same identity")
		self.canvases.append(cvs)

	def canvas(self, *args, **kw):
		"""Create Canvas and add to this Sequence."""
		cvs = self._factory.canvas(*args, **kw)
		self.add_canvas(cvs)
		return cvs

	def toJSON(self, top=True):
		"""Serialize as JSON."""
		json = super(Sequence, self).toJSON(top)
		newcvs = []
		for c in json['canvases']:
			if isinstance(c, Canvas):
				newcvs.append(c.toJSON(False))
			elif type(c) == dict and c['@type'] == 'sc:Canvas':
				newcvs.append(c)
			else:
				# break
				raise MetadataError("Non Canvas as part of Sequence")
		json['canvases'] = newcvs
		return json

class Canvas(ContentResource):
	"""Canvas object in Presentation API."""

	_type = "sc:Canvas"
	_uri_segment = "canvas/"	
	_required = ["@id", "label", "height", "width"]
	_warn = ["images"]
	height = 0
	width = 0
	images = []
	otherContent = []

	def __init__(self, *args, **kw):
		"""Initialize Canvas."""
		self.images = []
		self.otherContent = []
		self.height = 0
		self.width = 0
		return super(Canvas, self).__init__(*args, **kw)

	def set_hw(self, h,w):
		"""Set Canvas height and width."""
		self.height = h
		self.width = w

	def add_annotation(self, imgAnno):
		"""Add Annotation to this Canvas."""
		self.images.append(imgAnno)

	def add_annotationList(self, annoList):
		"""Add AnnotationList to this Canvas."""
		self.otherContent.append(annoList)

	def annotation(self, *args, **kw):
		"""Create Annotation and add to this Canvas."""
		anno = self._factory.annotation(*args, **kw)
		anno.on = self.id
		self.add_annotation(anno)
		return anno

	def annotationList(self, *args, **kw):
		"""Creata AnnotationList and add this Canvas."""
		annol = self._factory.annotationList(*args, **kw)
		annol._canvas = self
		self.add_annotationList(annol)
		return annol

	def toJSON(self, top=True):
		"""Serialize as JSON."""
		json = super(Canvas, self).toJSON(top)
		if 'images' in json:
			newimgs = []
			for c in json['images']:
				newimgs.append(c.toJSON(False))
			json['images'] = newimgs
		if 'otherContent' in json:
			newlists = []
			for c in json['otherContent']:
				newlists.append(c.toJSON(False))
			json['otherContent'] = newlists
		return json


class Annotation(BaseMetadataObject):
	"""Annotation object in Presentation API."""

	_type = "oa:Annotation"
	_uri_segment = "annotation/"
	_required = ["motivation", "resource", "on"]
	_warn = ["@id"]

	def __init__(self, *args, **kw):
		"""Initialize Annotation."""
		self.motivation = "sc:painting"
		self.on = ""
		self.resource = {}
		return super(Annotation, self).__init__(*args, **kw)

	def image(self, ident="", label="", iiif=False):
		"""Create Image body."""
		img = self._factory.image(ident, label, iiif)
		self.resource = img
		return img

	def text(self, text, language="", format="text/plain"):
		"""Creata Text body."""
		txt = self._factory.text(text, language, format)
		self.resource = txt
		return txt

	def audio(self, ident="", label=""):
		"""Create Audio body."""
		aud = self._factory.audio(ident, label)
		self.resource = aud
		return aud

	def choice(self, default, rest):
		"""Create Choice body."""
		chc = self._factory.choice(default, rest)
		self.resource = chc
		return chc

	def stylesheet(self, css, cls):
		"""Add stylesheet information for body."""
		# This has to go here, as need to modify both Annotation and Resource
		ss = { "@type": ["oa:CssStyle", "cnt:ContentAsText"], "format": "text/css", "chars" : css}
		self.stylesheet = ss
		if not self.resource:
			raise MetadataError("Cannot set a stylesheet without first creating the body")
		if isinstance(self.resource, SpecificResource):
			self.resource.style = cls
		else:
			sr = SpecificResource(self._factory, self.resource)
			sr.style = cls
			self.resource = sr

	def toJSON(self, top=True):
		"""Serialize as JSON."""
		json = super(Annotation, self).toJSON(top)
		json['resource'] = json['resource'].toJSON(top=False)
		if isinstance(json['on'], BaseMetadataObject):
			json['on'] = json['on'].toJSON(top=False)
		return json


class SpecificResource(BaseMetadataObject):
	"""Specific Resource in Presentation API."""

	_type = "oa:SpecificResource"
	_required = ['full']
	_warn = []
	style = ""
	selector = ""
	full = None

	def __init__(self, factory, full):
		"""Initialize SpecificResourec object."""
		self._factory = factory
		self.type = self.__class__._type
		self.full=full

	def toJSON(self, top=False):
		"""Serialize as JSON."""
		json = super(SpecificResource, self).toJSON(top)
		if isinstance(json['full'], BaseMetadataObject):
			json['full'] = json['full'].toJSON()
		return json



class ExternalText(ContentResource):
	"""External text object in Presentation API."""

	_type = "dcterms:Text"
	_required = []
	_factory = None
	_warn = ["format"]
	_uri_segment = "resources"

	format = ""
	language = ""

	def __init__(self, factory, ident, language="", format=""):
		"""Initialize ExternalText object.

		Builds full URI for self.id unless a full URI is supplied
		"""
		self._factory = factory
		self.format = format
		self.language = language
		self.type = self.__class__._type
		if is_http_uri(ident):
			self.id = ident
		else:
			self.id = self.id = factory.metadata_base + self.__class__._uri_segment + ident


class Text(ContentResource):
	"""Text (cnt:ContentAsText) resource."""

	_type = "cnt:ContentAsText"
	_required = ["chars"]
	_warn = ["format"]
	chars = ""
	format = ""
	language = ""

	def __init__(self, factory, text, language="", format="text/plain"):
		"""Initialize Text resource."""
		self._factory = factory
		self.type = self.__class__._type
		self.chars = text
		self.format = format
		if language:
			self.language = language

class Audio(ContentResource):
	"""Audio resource."""

	_type = "dctypes:Sound"
	_required = ["@id"]
	_warn = ["format"]
	_uri_segment = "res"

class Image(ContentResource):
	"""Image resource."""

	_type = "dctypes:Image"
	_required = ["@id"]
	_warn = ["format", "height", "width"]

	def __init__(self, factory, ident, label, iiif=False):
		"""Initialize Image resource."""
		self._factory = factory
		self.type = self.__class__._type
		self.label = ""
		self.format = ""
		self.height = 0
		self.width = 0
		self._identifier = ""
		if label:
			self.set_label(label)

		if iiif == True:
			# add IIIF service
			# ident is identifier
			self.id = factory.image_base + ident + '/full/full/0/native.jpg'
			self._identifier = ident
			self.format = "image/jpeg"
			self.service = {
				"@id": factory.image_base + ident,
			}
			if factory.iiif_version != -1:
				self.service['profile'] = factory.iiif_profile_uri

		else:
			# Static image
			# ident is either full URL or filename
			if is_http_uri(ident):
				self.id = ident
			else:
				self.id = factory.image_base + ident

	def set_hw(self, h,w):
		"""Set height and width to specified values."""
		self.height = h
		self.width = w

	def set_hw_from_iiif(self):
		"""Set height and width from IIIF Image Information."""
		if not self._identifier:
			raise ConfigurationError("Image is not configured with IIIF support")

		requrl = self._factory.image_base + self._identifier + '/info.json';
		try:
			fh = urllib.urlopen(requrl)
			data = fh.read()
			fh.close()
		except:
			raise ConfigurationError("Could not get IIIF Info from %s" % requrl)

		try:
			js = json.loads(data)
			self.height = int(js['height'])
			self.width = int(js['width'])
		except:
			raise ConfigurationError("Response from IIIF server did not have mandatory height/width")


	def set_hw_from_file(self, fn):
		"""Set height and width from image file."""
		# Try to do it automagically
		if not os.path.exists(fn):
			raise ValueError("Could not find image file: %s" % fn)

		cmd = self._factory.whichid
		if cmd:
			# Try ImageMagick
			try:
				info = subprocess.check_output(cmd + ' -ping -format "%h %w" ' + fn, shell=True).strip()
				(h, w) = info.split(" ")
				self.height = int(h)
				self.width = int(w)
				return
			except:
				pass

		if pil_image:
			# Try PIL
			try:
				img = pil_image.open(fn)
				(w,h) = img.size
				self.height = h
				self.width = w
				try:
					img.close()
				except:
					pass
				return
			except:
				pass

		raise ConfigurationError("No identify from ImageMagick and no PIL, you have to set manually")

class Choice(BaseMetadataObject):
	"""Open Annotation Choice object."""

	_type = "oa:Choice"
	_uri_segment = "annotation" # not really necessary
	_required = ["item"]
	_warn = ["default"]
	default = {}
	item = []

	def __init__(self, factory, default, rest):
		"""Initialize this Choice."""
		self.default = default
		if type(rest) != list:
			rest = [rest]
		self.item = rest
		return super(Choice, self).__init__(factory, indent="", label="", mdhash={})

	def toJSON(self, top=True):
		"""Serialize as JSON."""
		json = super(Choice, self).toJSON(top)
		json['default'] = json['default'].toJSON(top=False)
		newitem = []
		for c in json['item']:
			newitem.append(c.toJSON(False))
		json['item'] = newitem		
		return json

class AnnotationList(BaseMetadataObject):
	"""Annotation List in Presentation API."""

	_type = "sc:AnnotationList"
	_uri_segment = "list/"	
	_required = ["@id"]
	_warn = []
	_canvas = None
	resources = []
	within = {}

	def __init__(self, *args, **kw):
		"""Initialize Annotation List."""
		self.resources = []
		self.within = []
		self._canvas = None
		return super(AnnotationList, self).__init__(*args, **kw)

	def add_annotation(self, imgAnno):
		"""Add Annotation to this Annotation List."""
		self.resources.append(imgAnno)

	def annotation(self, *args, **kw):
		"""Creata Annotation in this Annotation List.

		Returns the Annotation
		"""
		anno = self._factory.annotation(*args, **kw)
		if self._canvas:
			anno.on = self._canvas.id
		self.add_annotation(anno)
		return anno

	def layer(self, *args, **kw):
		"""Create Layer that this Annotation List is within.

		Returns the Layer
		"""
		lyr = self._factory.layer(*args, **kw)
		self.within = lyr
		return lyr

	def toJSON(self, top=True):
		"""Serialize as JSON.

		if top == false, only include @id, @type, label
		else, include everything
		"""
		json = super(AnnotationList, self).toJSON(top)
		if top:
			newl = []
			for c in json['resources']:
				newl.append(c.toJSON(False))
			json['resources'] = newl
		else:
			del json['resources']
		return json


class Range(BaseMetadataObject):
	"""Range object in Presentation API."""

	_type = "sc:Range"
	_uri_segment = "range/"	
	_required = ["@id", "label", "canvases"]
	_warn = []
	canvases = []

	def __init__(self, factory, ident="", label="", mdhash={}):
		"""Initialize Range."""
		super(Range, self).__init__(factory, ident, label, mdhash)
		self.canvases = []	

	def add_canvas(self, cvs, frag=""):
		"""Add Canvas to this Range."""
		cvsid = cvs.id
		if frag:
			cvsid += frag
		self.canvases.append(cvsid)


class Layer(BaseMetadataObject):
	"""Layer object in Presentation API."""

	_type = "sc:Layer"		
	_uri_segment = "layer/"
	_required = ["@id", "label"]
	_warn = []


