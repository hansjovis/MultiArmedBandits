from config import config

class MetaModel:
	""" Metamodels are a kind of ensemble,
		They train models, evaluate which works best,
		And then extend the best one,
		Repeat.
	"""
	def __init__(self, opts=None, models=None):
		""" Constructor which prepares for the run.
			@param opts {dict} with options.
					If None or missing values, defaults are used.
			@param models {Model or iterable} models to initialize run.
					If None, will start with an empty model.
			@return {MetaModel} self
		"""
		# Set opts
		metaconf = config.metamodel
		self.opts = opts if opts is not None else {}
		for key in metaconf:
			if key not in self.opts:
				self.opts.update({key: metaconf[key]})
		# Set models
		self.models = models if models is not None else self.extend(Model())
	
	def run(self):
		""" Starts training until stopping criteria are met.
			The main loop works as follows:
			@return {Model} The winner model
		"""
		while True:
			self.train()
			model, stop = self.evaluate()
			if stop:
				return model
			self.models = self.extend(model)
	
	def train(self):
		""" Make the models explore.
			@return {void} This function changes self.models
		"""
		run_id = random.randint(self.opts['run_id_min'], self.opts['run_id_max'])
		for i in range(self.opts['trainits']):
			context = serverCommunication.getContext(run_id, i)
			choices = [model.choose(context, 1) for model in self.models]
			for model, choice in zip(self.models, choices):
				result = serverCommunication.proposePage(
												run_id, i, choice['header'],
										 choice['adtype'], choice['color'], 
									  choice['productid'], choice['price'])
				model.learn(context, choice, result)
	
	def evaluate(self):
		""" Evaluate the models by making them exploit and pick the best.
			@return {Model} The best model
					{Boolean} Have we converged?
		"""
		run_id = random.randint(self.opts['run_id_min'], self.opts['run_id_max'])
		results = [0]*len(self.models)
		for i in range(self.opts['testits']):
			context = serverCommunication.getContext(run_id, i)
			choices = [model.choose(context, 0) for model in self.models]
			for j, choice in enumerate(choices):
				results[j] += serverCommunication.proposePage(
								run_id, i, choice['header'],
						 choice['adtype'], choice['color'], 
					  choice['productid'], choice['price'])
		return self.models[np.argmax(results)], self.hasconverged(results)
	
	def extend(self, model):
		""" Generate new models by extending model with random variables.
			@param model {Model} The model to extend.
			@return {iterable Model} The extended models.
		"""
		# Grab all variables not in model
		variables = list(set(config.variables).difference(set(model.variables)))
		models = [deepcopy(model) for i in range(len(variables))]
		for v, m in zip(variables, models):
			m.extend(v)
		return models

	def hasconverged(self, results):
		""" Check if the results have improved.
			TODO: This can be a lot better.
		"""
		return max(results) < self.opts['conv_threshold'] * mean(results)

class Model:
    """ Abstract model class
    """

    def __init__(self):
        """ Generic constructor """
        pass
    
    def choose(self, context, epsilon):
        """ Makes a choice of the five ad variables given context
            With probability epsilon:
                to minimize entropy in the data
            Else:
                to maximize expected gain
            @param context {dict} containing context variables
            @param epsilon {float} exploration probability
            @return {dict} containing choice values
        """
        pass

    def learn(self, context, choices, result):
        """ Updates the model given the context, choices and result
            @param context {dict} containing context variables
            @param choices {dict} containing variables from last choose
            @param result {float} gain (succes * reward)
            @return {void} his function changes the object
        """
        pass
    
    def extend(self, var):
        """ Extend the model with variable var
            @param var {string} variable from context or choices
            @return {void} this function changes the object
        """
        pass
