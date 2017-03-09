"""IIIF Presentation API resource loader."""

from __future__ import unicode_literals
import os

from .factory import ManifestFactory, Service
from .factory import PresentationError, MetadataError, ConfigurationError, StructuralError, RequirementError, DataError
from .json_with_order import json, OrderedDict
from .util import is_http_uri, STR_TYPES

try: #python2
    # Must try this first as io also exists in python2
    # but in the wrong one!
    import StringIO as io
except ImportError: #python3
    import io

try:
	from pyld import jsonld
except:
	jsonld = None


class SerializationError(PresentationError):
	"""Errors found while loading IIIF resource."""

	pass

def load_document_local(url):
	"""Load local copy of context document with given url.

	Returns dict with three elements 'contextUrl'=None, 
	'documentUrl'=None and 'document' set to data read
	"""
	doc = { 'contextUrl': None,
			'documentUrl': None,
			'document': '' }
	contexts_dir = os.path.join(os.path.dirname(__file__),'contexts')
	if url == "http://iiif.io/api/presentation/2/context.json":
		fn = os.path.join(contexts_dir,'context_21.json')
	else:
		fn = os.path.join(contexts_dir,'context_10.json')
	fh = open(fn)
	data = fh.read()
	fh.close()
	doc['document'] = data;
	return doc
		
if jsonld:
	jsonld.set_document_loader(load_document_local)

class ManifestReader(object):
	"""Read manifest of other presentation API resource."""

	contexts = {
		'0.9': 'http://www.shared-canvas.org/ns/context.json',
		'1.0': 'http://www.shared-canvas.org/ns/context.json',
		'2.0': 'http://iiif.io/api/presentation/2/context.json',
		'2.1': 'http://iiif.io/api/presentation/2/context.json'
	}

	def __init__(self, data, version=None):
		"""Initialize with data and optional version.

		data may be either a string or parsed data
		"""
		self.data = data
		self.debug_stream = None
		self.require_version = version

	def buildFactory(self, version):
		"""Return instance of ManifestFactory for correct API version."""
		if self.require_version:
			fac = ManifestFactory(version=self.require_version)
		else:
			fac = ManifestFactory(version=version)
		self.debug_stream = io.StringIO()
		fac.set_debug("warn")
		fac.set_debug_stream(self.debug_stream)
		return fac

	def getVersion(self, js):
		"""Get Presentation API version from @context.

		Throws a SerializationError if there is no @context
		"""
		if ('@context' not in js):
			raise SerializationError('Top level resource MUST have @context', js)
		ctx = js['@context']
		# Allow list of contexts, and iterate
		if type(ctx) != list:
			ctx = [ctx]

		versions = []
		for c in ctx:
			for k,v in self.contexts.items():
				if c == v:
					versions.append(k)
					
		if not versions:
			raise SerializationError('Top level @context is not known', js)
		if self.require_version and self.require_version not in versions:
			raise SerializationError('Expected version %s context, got version %s' % (self.require_version, versions))
		versions.sort()
		return versions

	def get_warnings(self):
		"""Get list of warning from debug stream."""
		if self.debug_stream:
			self.debug_stream.seek(0)
			return self.debug_stream.readlines()	
		else:
			return []

	def read(self):
		"""Read Presentation API resource."""
		data = self.data
		if not data:
			raise SerializationError("No data provided", data)

		if type(data) in [dict, OrderedDict]:
			js = data
		else:
			try:
				js = json.loads(data)
			except:
				# could be badly encoded utf-8 with BOM
				try:
					data = data.decode('utf-8')
				except:
					#Py3 does not have decode on str which is unicode already
					pass	
				if data[0] == u'\ufeff':
					data = data[1:].strip()
				try:
					js = json.loads(data)
				except:
					raise SerializationError("Data is not valid JSON", data)				

		# Try to see if we're valid JSON-LD before further testing

		versions = self.getVersion(js)
		if self.require_version:
			factory = self.buildFactory(self.require_version)
		else:
			factory = self.buildFactory(versions[-1])
		self.factory = factory
		top = self.readObject(js)
		if jsonld:
			try:
				jsonld.expand(js)
			except Exception as e:
				raise
				raise SerializationError("Data is not valid JSON-LD: %r" % e, data)
		return top


	def jsonld_to_langhash(self, js):
		"""Convert JSON-LD language into a dict of value indexed by language."""
		# convert from @language/@value[/@type]
		# to {lang[ type]: value}
		if type(js) in STR_TYPES:
			return js
		elif '@value' not in js:
			raise DataError("Missing @value for string", js)
		else:
			if '@language' in js:
				lh = {js['@language']:js['@value']}				
			else:
				lh = js['@value']
			return lh

	def readObject(self, js, parent=None, parentProperty=None):
		"""Recursively find top level object type, and build it in Factory."""
		if not parent:
			parent = self.factory

		ident = js.get('@id', '')
		try:
			typ = js['@type']
		except:
			if parentProperty != 'service':
				raise RequirementError('Every resource must have @type', parent)
			else:
				typ = ''

		# Black magic: 'sc:AnnotationList' --> parent.annotationList()
		cidx = typ.find(':')
		if cidx > -1:
			fn = typ[cidx+1].lower() + typ[cidx+2:]
		elif parentProperty == 'service':
			fn = 'add_service'
		else:
			raise StructuralError("Unknown resource class " + typ, parent)

		if hasattr(parent, fn):
			func = getattr(parent, fn)
			try:
				what = func(ident=ident)
			except ConfigurationError:
				# This is thrown when there is an ident, but it's not HTTP
				raise RequirementError("The identifier '%s' is not an HTTP(S) URI" % ident, None)
			except TypeError:
				if fn == "choice":
					# Have to construct default and items first
					deflt = self.readObject(js['default'], parent, 'default')
					itm = js['item']
					itms = []
					if type(itm) == list:
						for i in itm:
							if type(i) == dict:
								itms.append(self.readObject(i, parent, 'item'))
							else:
								itms.append(i)
					else:
						if type(itm) == dict:
							itms.append(self.readObject(itm, parent, 'item'))
						else:
							itms = [itm]
					what = func(deflt, itms)
					# We're done
					return what
				else:
					what = func()
		elif fn == "specificResource":
			try:
				fullo = self.readObject(js['full'], parent)
			except StructuralError:
				# Use Case: Canvas with FragmentSelector
				# XXX Figure this out
				raise				
			try:
				what = fullo.make_selection(js['selector'])
				if 'style' in js:
					what.style = js['style']
			except:
				# no selector, so just style ... already past the annotation...
				what = self.factory.specificResource(fullo)
				what.style = js['style']
			# need to explicitly set @id because we didn't call with a func(ident=)
			if '@id' in js:
				what.id = js['@id']
			setattr(parent, parentProperty, what)
			return what
		elif fn == "contentAsText":
			fn = 'text'
			func = getattr(parent, fn)
			text = js.get('chars', '')
			ident = js.get('@id', '')
			language = js.get('language', '')
			format = js.get('format', '')
			what = func(text, ident, language, format)
		elif hasattr(self.factory, fn):
			# dctypes:Image --> factory.image(ident)
			# dctypes:Audio --> factory.audio(ident)
			func = getattr(self.factory, fn)
			what = func(ident)
			# Normally done by hierarchy, but we're from the factory direct
			setattr(parent, parentProperty, what)
		else:
			raise StructuralError("Unknown resource class " + typ + " from parent: " + parent._type, parent)

		# Up front check for required properties in the INCOMING data
		for req in what._required:
			if req not in js:
				if req in what._structure_properties:
					# If we're minimal in our parent, then allow missing structure
					if parentProperty and parent._structure_properties.get(parentProperty, {}).get('minimal', False):
						continue
					if req == 'canvases' and len(parent.sequences) > 1:
						# Do not Allow second and future sequences if not minimal
						continue
					raise StructuralError("%s['%s'] not present and required" % (what._type, req), what)
				else:
					raise RequirementError("%s['%s'] not present and required" % (what._type, req), what)
			elif req == "canvases" and len(parent.sequences) > 1:
				raise StructuralError("Second Sequence must not list canvases", what)

		# Configure the object from JSON
		kvs = sorted(js.items())
		for (k,v) in kvs:
			# Recurse
			if k in what._structure_properties:
				if type(v) == list:
					for sub in v:
						if type(sub) in [dict, OrderedDict]:
							subo = self.readObject(sub, what, k)
						elif is_http_uri(sub):
							# pointer to a resource (eg canvas in structures)
							# Use magic setter to ensure listiness
							if k in what._structure_properties:
								# super meta black magic
								kls = what._structure_properties[k]['subclass'].__name__.lower()
								addfn = getattr(what, "add_%s" % kls)
								addfn(sub)
							else:
								what._set_magic_resource(k, sub)
						else:
							raise StructuralError("Can't create object for: %r" % sub, what)
				elif what._structure_properties[k].get('list', False):
					raise StructuralError("%s['%s'] must be a list, got: %s" % (what._type, k, v), what)
				elif type(v) in [dict, OrderedDict]:
					subo = self.readObject(v, what, k)
				elif type(v) in STR_TYPES and (is_http_uri(v) or v.startswith('urn:') or v.startswith('_:')):
					setattr(what, k, v)
				else:
					raise StructuralError("%s['%s'] has broken value: %r" % (what._type, k, v), what )

			# Object properties
			elif k in what._object_properties:
				if type(v) == list:
					for sub in v:
						setattr(what, k, sub)
				else:
					setattr(what, k, v)

			# Skip past magic keys we've already processed
			elif k in ['@id', '@type']:
				continue
			elif k == '@context':
				if isinstance(what, Service):
					setattr(what, 'context', v)
				else:
					continue
			# Process metadata pairs
			elif k  == 'metadata':
				if type(v) == list:
					for item in v:
						iv = item['value']
						if type(iv) == dict:
							iv = self.jsonld_to_langhash(iv)
						il = item['label']
						if type(il) == dict:
							il = self.jsonld_to_langhash(il)
							lh = {'label': il, 'value': iv}
						elif type(il) == list:
							# oh man :(
							lh = {'label': il, 'value': iv}
						else:
							lh = {il: iv}
						what.set_metadata(lh)
				else:
					# Actually this is an error
					raise DataError("Metadata must be a list", what)
			# Process descriptive fields
			elif k in ['label', 'attribution', 'description']:
				# need to reverse the language magic
				kfn = getattr(what, "set_%s" % k)
				if type(v) == list:
					nlist = []
					for item in v:
						# {@value:bla, @language:en}
						lh = self.jsonld_to_langhash(item)
						nlist.append(lh)
					kfn(nlist)
				elif type(v) in STR_TYPES:
					kfn(v)
				elif type(v) == dict:
					kfn(self.jsonld_to_langhash(v))
				else:
					raise DataError("Unknown type for %s" % k, what)

			elif k == 'startCanvas':
				what.set_start_canvas(v)
			elif k in ['agent', 'date', 'location']:
				# XXX Magically upgrade 0.9?
				if self.require_version and self.require_version != "0.9":
					raise RequirementError("Old property from 0.9 seen: %s expected version %s" % (k, self.require_version))
				pass
			elif k == "resources":
				# XXX Used in full annotation list response
				pass

			else:
				setattr(what, k, v)

		return what
