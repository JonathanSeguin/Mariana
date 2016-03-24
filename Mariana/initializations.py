import numpy, time
import theano
import theano.tensor as tt
import Mariana.settings as MSET

__all__= [
	"Initialization_ABC",
	"GlorotTanhInit",
	"Uniform",
	"UniformWeights",
	"UniformEmbeddings",
	"SmallUniform",
	"SmallUniformWeights",
	"SmallUniformEmbeddings",
	"Normal",
	"NormalWeights",
	"TiedTransposeWeights",
	"TiedSameWeights",
	"Value",
	"ValueWeights"
	"ValueBias",
	"ZerosWeights",
	"ZerosBias"
]

class Initialization_ABC(object) :
	"""This class defines the interface that an Initialization must offer. As a general good practice every init should only take care of a single
	parameter, but you are free to do whatever you want. 
	"""

	def __init__(self, *args, **kwargs) :
		self.hyperParameters = []
		self.name = self.__class__.__name__
		
	def __call__(self, *args, **kwargs) :
		self.initialize(*args, **kwargs)

	def initialize(self, layer) :
		"""The function that all Initialization_ABCs must implement"""
		raise NotImplemented("This one should be implemented in child")

class GlorotTanhInit(Initialization_ABC) :
	"""Set up the layer weights according to the tanh initialisation introduced by Glorot et al. 2010"""
	def __init__(self, *args, **kwargs) :
		Initialization_ABC.__init__(self, *args, **kwargs)

	def initialize(self, layer) :
		rng = numpy.random.RandomState(MSET.RANDOM_SEED)
		layer.W = rng.uniform(
					low = -numpy.sqrt(6. / (layer.nbInputs + layer.nbOutputs)),
					high = numpy.sqrt(6. / (layer.nbInputs + layer.nbOutputs)),
					size = (layer.nbInputs, layer.nbOutputs)
				)

class Uniform(Initialization_ABC) :
	"""Random values from a unifrom distribution (divided by the overall sum)."""
	def __init__(self, parameter, shape, *args, **kwargs) :
		Initialization_ABC.__init__(self, *args, **kwargs)
		self.parameter = parameter
		self.shape = shape
		self.hyperParameters = ['parameter']

	def initialize(self, layer) :
		v = numpy.random.random(self.shape)
		v = numpy.asarray(v, dtype=theano.config.floatX)
		setattr( layer, self.parameter,  theano.shared(value = v, name = "%s_%s" + (self.parameter, layer.name) ) )

class UniformWeights(Uniform) :
	"""Small random weights from a unifrom distribution"""
	def __init__(self, *args, **kwargs) :
		Uniform.__init__(self, 'W', None, *args, **kwargs)
		self.hyperParameters = []

	def initialize(self, layer) :
		self.shape = (layer.nbInputs, layer.nbOutputs)
		Uniform.initialize(self, layer)

class UniformEmbeddings(Uniform) :
	"""Random embeddings from a unifrom distribution"""
	def __init__(self, *args, **kwargs) :
		Uniform.__init__(self, 'embeddings', None, *args, **kwargs)
		self.hyperParameters = []

	def initialize(self, layer) :
		self.shape = (layer.dictSize, layer.nbDimensions)
		Uniform.initialize(self, layer)

class SmallUniform(Uniform) :
	"""Random values from a unifrom distribution (divided by the overall sum)."""
	def initialize(self, layer) :
		v = numpy.random.random(self.shape)
		v /= sum(v)
		v = numpy.asarray(v, dtype=theano.config.floatX)
		setattr( layer, self.parameter,  theano.shared(value = v, name = "%s_%s" + (self.parameter, layer.na

class SmallUniformWeights(SmallUniform) :
	"""Small random weights from a unifrom distribution (divided by the overall sum)"""
	def __init__(self, *args, **kwargs) :
		SmallUniform.__init__(self, 'W', None, *args, **kwargs)
		self.hyperParameters = []

	def initialize(self, layer) :
		self.shape = (layer.nbInputs, layer.nbOutputs)
		SmallUniform.initialize(self, layer)

class SmallUniformEmbeddings(SmallUniform) :
	"""Small random embeddings from a unifrom distribution (divided by the overall sum)"""
	def __init__(self, *args, **kwargs) :
		SmallUniform.__init__(self, 'embeddings', None, *args, **kwargs)
		self.hyperParameters = []

	def initialize(self, layer) :
		self.shape = (layer.dictSize, layer.nbDimensions)
		SmallUniform.initialize(self, layer

class Normal(Initialization_ABC) :
	"""Random values from a normal distribution"""
	def __init__(self, parameter, standardDev, shape, *args, **kwargs) :
		Initialization_ABC.__init__(self, *args, **kwargs)
		self.parameter = parameter
		self.shape = shape
		self.standardDev = standardDev
		self.hyperParameters = ["parameter", "standardDev"]

	def initialize(self, layer) :
		v = nnumpy.random.normal(0, self.standardDev, (layer.nbInputs, layer.nbOutputs))
		setattr( layer, self.parameter,  theano.shared(value = v, name = "%s_%s" + (self.parameter, layer.name) ) )

class NormalWeights(Normal) :
	"""Random weights from a normal distribution"""
	def __init__(self, standardDev, *args, **kwargs) :
		Normal.__init__(self, 'W', None, *args, **kwargs)
		self.standardDev = standardDev
		self.hyperParameters = ["standardDev"]

	def initialize(self, layer) :
		self.shape = (layer.nbInputs, layer.nbOutputs)
		Normal.initialize(self, layer)

class TiedTransposeWeights(Initialization_ABC) :
	"""Initialize the weights to be the transpose of a another layer weights"""
	def __init__(self, otherLayer, *args, **kwargs) :
		Initialization_ABC.__init__(self, *args, **kwargs)
		self.otherLayer = otherLayer
		self.otherLayerName = otherLayer.nane
		self.hyperParameters.append("otherLayerName")

	def initialize(self, layer) :
		layer.W = self.otherLayer.W.T

class TiedSameWeights(Initialization_ABC) :
	"""Initialize the weights to be the same as the weights of a another layer weights"""
	def __init__(self, otherLayer, *args, **kwargs) :
		Initialization_ABC.__init__(self, *args, **kwargs)
		self.otherLayer = otherLayer
		self.otherLayerName = otherLayer.nane
		self.hyperParameters.append("otherLayerName")

	def initialize(self, layer) :
		layer.W = self.otherLayer.W

class Value(Initialization_ABC) :
	"""Initialize to a given value"""
	def __init__(self, parameter, shape, value, *args, **kwargs) :
		Initialization_ABC.__init__(self, *args, **kwargs)
		self.parameter = parameter
		self.shape = shape
		self.value = value
		self.hyperParameters = ["parameter", "value"]

	def initialize(self, layer) :
		v = numpy.zeros(
					self.shape,
					dtype = theano.config.floatX
				) + value
		
		setattr( layer, self.parameter,  theano.shared(value = v, name = "%s_%s" + (self.parameter, layer.name) ) )

class ValueWeights(Value) :
	"""Initialize the weights to a given value"""
	def __init__(self, value, *args, **kwargs) :
		Value.__init__(self, 'W', None, value, *args, **kwargs)
		self.hyperParameters = ["value"]

	def initialize(self, layer) :
		self.shape = (layer.nbInputs, layer.nbOutputs)
		Value.initialize(self, layer)

class ZerosWeights(ValueWeights) :
	"""Initialize the weights to zero"""
	def __init__(self, value, *args, **kwargs) :
		ValueWeights.__init__(self, 0)
		self.hyperParameters = []

class ValueBias(Initialization_ABC) :
	"""Initialize the bias to a given value"""
	def __init__(self, values, *args, **kwargs) :
		Value.__init__(self, 'b', None, value, *args, **kwargs)
		self.hyperParameters = ["value"]

	def initialize(self, layer) :
		self.shape = (layer.nbOutputs,)
		Value.initialize(self, layer)

class ZerosBias(ValueBias) :
	"""Initialize the bias to zeros"""
	def __init__(self, *args, **kwargs) :
		ValueBias.__init__(self, value)
		self.hyperParameters = []